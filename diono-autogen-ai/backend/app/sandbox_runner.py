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


class SandboxRunner:
    """Secure code execution in Docker containers"""
    
    def __init__(self):
        try:
            self.client = docker.from_env()
            logger.info("Docker client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Docker client: {e}")
            self.client = None
    
    def _get_image_for_language(self, language: str) -> str:
        """Get Docker image for programming language"""
        images = {
            "python": "python:3.11-slim",
            "javascript": "node:18-alpine",
            "typescript": "node:18-alpine",
            "java": "openjdk:17-slim",
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
            "typescript": ["ts-node", filename],
            "java": ["java", filename],
            "go": ["go", "run", filename],
            "rust": ["rustc", filename, "&&", "./main"],
            "ruby": ["ruby", filename],
            "php": ["php", filename],
        }
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
    
    async def execute(
        self,
        code: str,
        language: str = "python",
        timeout: int = None,
        workspace: Optional[str] = None
    ) -> CodeExecutionResponse:
        """Execute code in sandbox"""
        if not self.client:
            return CodeExecutionResponse(
                success=False,
                output="",
                error="Docker client not available",
                execution_time=0.0
            )
        
        timeout = timeout or settings.MAX_EXECUTION_TIME
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
                
                # Run container
                container = self.client.containers.run(
                    image,
                    command=command,
                    volumes=volumes,
                    working_dir="/workspace",
                    mem_limit=settings.SANDBOX_MEMORY_LIMIT,
                    cpu_quota=int(settings.SANDBOX_CPU_LIMIT * 100000),
                    network_disabled=False,  # Allow network for package installation
                    detach=True,
                    remove=True
                )
                
                # Wait for completion with timeout
                try:
                    result = container.wait(timeout=timeout)
                    logs = container.logs().decode('utf-8')
                    
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
    
    def cleanup(self):
        """Cleanup Docker resources"""
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
