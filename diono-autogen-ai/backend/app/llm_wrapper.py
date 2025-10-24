"""
LLM integration wrapper for open-source models
"""
from typing import Optional, Dict, Any, AsyncGenerator
import httpx
import json
from loguru import logger
from .config import settings


class LLMWrapper:
    """Wrapper for open-source LLM APIs"""
    
    def __init__(
        self,
        model: str = None,
        api_url: str = None,
        api_key: Optional[str] = None
    ):
        self.model = model or settings.LLM_MODEL
        self.api_url = api_url or settings.LLM_API_URL
        self.api_key = api_key or settings.LLM_API_KEY
        self.client = httpx.AsyncClient(timeout=300.0)
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = None,
        max_tokens: int = None,
        stream: bool = False
    ) -> str | AsyncGenerator[str, None]:
        """Generate response from LLM"""
        temperature = temperature or settings.LLM_TEMPERATURE
        max_tokens = max_tokens or settings.LLM_MAX_TOKENS
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        if stream:
            return self._generate_stream(messages, temperature, max_tokens)
        else:
            return await self._generate_complete(messages, temperature, max_tokens)
    
    async def _generate_complete(
        self,
        messages: list,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Generate complete response"""
        try:
            # Support for Ollama API format
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False
            }
            
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            response = await self.client.post(
                f"{self.api_url}/v1/chat/completions",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise
    
    async def _generate_stream(
        self,
        messages: list,
        temperature: float,
        max_tokens: int
    ) -> AsyncGenerator[str, None]:
        """Generate streaming response"""
        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True
            }
            
            headers = {"Content-Type": "application/json"}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with self.client.stream(
                "POST",
                f"{self.api_url}/v1/chat/completions",
                json=payload,
                headers=headers
            ) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                            if "choices" in chunk and len(chunk["choices"]) > 0:
                                delta = chunk["choices"][0].get("delta", {})
                                if "content" in delta:
                                    yield delta["content"]
                        except json.JSONDecodeError:
                            continue
        
        except Exception as e:
            logger.error(f"LLM streaming failed: {e}")
            raise
    
    async def generate_plan(self, description: str, requirements: list = None) -> Dict[str, Any]:
        """Generate a build plan from description"""
        system_prompt = """You are an expert software architect. Generate a detailed build plan.
        
Your response must be valid JSON with this structure:
{
    "steps": [
        {"step": 1, "title": "...", "description": "...", "files": ["..."], "estimated_minutes": 10}
    ],
    "tech_stack": ["python", "fastapi", "react"],
    "file_structure": {
        "backend/": {"app.py": "Main application"},
        "frontend/": {"App.jsx": "Main component"}
    },
    "estimated_time": 120
}"""
        
        req_text = ""
        if requirements:
            req_text = f"\n\nSpecific requirements:\n" + "\n".join(f"- {r}" for r in requirements)
        
        prompt = f"""Create a detailed build plan for: {description}{req_text}

Provide a step-by-step implementation plan with file structure and time estimates."""
        
        response = await self.generate(prompt, system_prompt=system_prompt)
        
        # Extract JSON from response
        try:
            # Try to find JSON in the response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                # Fallback: create basic plan
                return {
                    "steps": [
                        {
                            "step": 1,
                            "title": "Setup project structure",
                            "description": "Create basic project files and directories",
                            "files": ["README.md", "requirements.txt"],
                            "estimated_minutes": 15
                        }
                    ],
                    "tech_stack": ["python"],
                    "file_structure": {"src/": {"main.py": "Main application"}},
                    "estimated_time": 60
                }
        except json.JSONDecodeError:
            logger.error("Failed to parse LLM response as JSON")
            raise ValueError("Invalid plan format from LLM")
    
    async def generate_code(
        self,
        task_description: str,
        language: str = "python",
        context: Optional[str] = None
    ) -> str:
        """Generate code for a specific task"""
        system_prompt = f"""You are an expert {language} programmer. Generate clean, well-documented code.
        
Rules:
1. Only output the code, no explanations
2. Include necessary imports
3. Add comments for complex logic
4. Follow best practices for {language}"""
        
        context_text = f"\n\nContext:\n{context}" if context else ""
        prompt = f"""Generate {language} code for: {task_description}{context_text}"""
        
        return await self.generate(prompt, system_prompt=system_prompt)
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


# Global LLM instance
llm = LLMWrapper()
