"""
Secure code execution sandbox using Docker
"""
import docker
import tempfile
import os
from pathlib import Path
from typing import Optional, Dict, Any
from loguru import logger
from .config import settings
from .models import CodeExecutionResponse
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor


class SandboxRunner:
    """Secure code execution in Docker containers"""
    
    def __init__(self):
        try:
            self.client = docker.from_env()
            # Thread pool for non-blocking execution (configurable size)
            self.executor = ThreadPoolExecutor(max_workers=settings.SANDBOX_MAX_WORKERS)
            logger.info(f"Docker client initialized with {settings.SANDBOX_MAX_WORKERS} workers")
        except Exception as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            self.client = None
            self.executor = None
    
    def _get_image_for_language(self, language: str) -> str:
        """Get Docker image for programming language"""
        images = {
            "python": "python:3.11-slim",
            "javascript": "node:18-alpine",
            "typescript": "node:18-alpine",
            "java": "openjdk:17-jdk-slim",  # JDK includes javac compiler
            "go": "golang:1.21-alpine",
            "rust": "rust:1.75-slim",
            "ruby": "ruby:3.2-slim",
            "php": "php:8.2-cli",
        }
        return images.get(language.lower(), "python:3.11-slim")
    
    def _get_command_for_language(self, language: str, filename: str) -> list:
        """Get execution command for language"""
        commands = {
            "python": ["python", filename],
            "javascript": ["node", filename],
            "ruby": ["ruby", filename],
            "php": ["php", filename],
            "go": ["go", "run", filename],
        }
        
        # Compiled languages need shell commands
        if language.lower() == "rust":
            return ["/bin/sh", "-c", f"rustc {filename} && ./code"]
        elif language.lower() == "java":
            # Extract class name from filename
            class_name = filename.replace(".java", "")
            return ["/bin/sh", "-c", f"javac {filename} && java {class_name}"]
        elif language.lower() == "typescript":
            # TypeScript requires ts-node (will be installed on first run)
            # Note: First execution may be slow due to package installation
            return ["/bin/sh", "-c", f"npx --yes ts-node {filename}"]
        
        return commands.get(language.lower(), ["python", filename])
    
    def _get_file_extension(self, language: str) -> str:
        """Get file extension for language"""
        extensions = {
            "python": ".py",
            "javascript": ".js",
            "typescript": ".ts",
            "java": ".java",
            "go": ".go",
            "rust": ".rs",
            "ruby": ".rb",
            "php": ".php",
        }
        return extensions.get(language.lower(), ".py")
    
    def _execute_sync(
        self,
        code: str,
        language: str,
        timeout: int,
        workspace: Optional[str]
    ) -> CodeExecutionResponse:
        """Synchronous execution logic (runs in thread pool)"""
        if not self.client:
            return CodeExecutionResponse(
                success=False,
                output="",
                error="Docker client not available",
                execution_time=0.0
            )
        
        start_time = time.time()
        
        try:
            # Create temporary directory for code
            with tempfile.TemporaryDirectory() as tmpdir:
                # Write code to file
                ext = self._get_file_extension(language)
                code_file = Path(tmpdir) / f"code{ext}"
                code_file.write_text(code)
                
                # Get Docker image and command
                image = self._get_image_for_language(language)
                command = self._get_command_for_language(language, f"code{ext}")
                
                # Pull image if not available
                try:
                    self.client.images.get(image)
                except docker.errors.ImageNotFound:
                    logger.info(f"Pulling Docker image: {image}")
                    self.client.images.pull(image)
                
                # Mount workspace if provided
                volumes = {tmpdir: {"bind": "/workspace", "mode": "rw"}}
                if workspace:
                    volumes[workspace] = {"bind": "/data", "mode": "rw"}
                
                # Run container (remove=False to safely capture logs)
                container = self.client.containers.run(
                    image,
                    command=command,
                    volumes=volumes,
                    working_dir="/workspace",
                    mem_limit=settings.SANDBOX_MEMORY_LIMIT,
                    cpu_quota=int(settings.SANDBOX_CPU_LIMIT * 100000),
                    network_disabled=not settings.SANDBOX_NETWORK_ENABLED,
                    detach=True,
                    remove=False  # Don't auto-remove to avoid log retrieval race
                )
                
                # Wait for completion with timeout
                try:
                    result = container.wait(timeout=timeout)
                    logs = container.logs().decode('utf-8')
                    
                    # Clean up container after capturing logs
                    try:
                        container.remove()
                    except:
                        pass
                    
                    execution_time = time.time() - start_time
                    
                    if result['StatusCode'] == 0:
                        return CodeExecutionResponse(
                            success=True,
                            output=logs,
                            error=None,
                            execution_time=execution_time
                        )
                    else:
                        return CodeExecutionResponse(
                            success=False,
                            output=logs,
                            error=f"Exit code: {result['StatusCode']}",
                            execution_time=execution_time
                        )
                
                except Exception as e:
                    # Timeout or other error
                    try:
                        container.stop(timeout=1)
                        container.remove()
                    except:
                        pass
                    
                    execution_time = time.time() - start_time
                    return CodeExecutionResponse(
                        success=False,
                        output="",
                        error=f"Execution timeout or error: {str(e)}",
                        execution_time=execution_time
                    )
        
        except Exception as e:
            logger.error(f"Sandbox execution failed: {e}")
            execution_time = time.time() - start_time
            return CodeExecutionResponse(
                success=False,
                output="",
                error=str(e),
                execution_time=execution_time
            )
    
    async def execute(
        self,
        code: str,
        language: str = "python",
        timeout: int = None,
        workspace: Optional[str] = None
    ) -> CodeExecutionResponse:
        """Execute code in sandbox (non-blocking)"""
        timeout = timeout or settings.MAX_EXECUTION_TIME
        
        # Run blocking Docker operations in thread pool
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            self.executor,
            self._execute_sync,
            code,
            language,
            timeout,
            workspace
        )
        return result
    
    def cleanup(self):
        """Cleanup Docker resources"""
        # Shutdown thread pool
        if self.executor:
            try:
                self.executor.shutdown(wait=False)
                logger.info("Thread pool shutdown complete")
            except Exception as e:
                logger.error(f"Thread pool shutdown failed: {e}")
        
        # Cleanup Docker containers
        if self.client:
            try:
                # Remove stopped containers
                for container in self.client.containers.list(all=True, filters={"status": "exited"}):
                    try:
                        container.remove()
                    except:
                        pass
            except Exception as e:
                logger.error(f"Cleanup failed: {e}")


# Global sandbox instance
sandbox = SandboxRunner()
