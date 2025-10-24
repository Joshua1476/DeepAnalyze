"""
LLM integration wrapper with multi-provider support
"""
from typing import Optional, Dict, Any, AsyncGenerator
import httpx
import json
from loguru import logger
from .config import settings
from .llm_providers import get_provider


class LLMWrapper:
    """Wrapper for multi-provider LLM APIs"""
    
    def __init__(
        self,
        provider: str = None,
        model: str = None,
        api_url: str = None,
        api_key: Optional[str] = None
    ):
        self.provider_type = provider or settings.LLM_PROVIDER
        self.model = model or settings.LLM_MODEL
        
        # Normalize API URL (strip trailing /v1 if present for OpenAI-compatible)
        base_url = (api_url or settings.LLM_API_URL).rstrip('/')
        if base_url.endswith('/v1') and self.provider_type in ['openai', 'anthropic', 'groq', 'together', 'openrouter', 'qwen', 'deepseek']:
            base_url = base_url[:-3]
            logger.warning(f"Stripped /v1 from LLM_API_URL: {base_url}")
        
        self.api_url = base_url
        self.api_key = api_key or settings.LLM_API_KEY
        
        # Get the appropriate provider
        self.provider = get_provider(self.provider_type, self.api_url, self.api_key)
        logger.info(f"Initialized LLM provider: {self.provider_type} with model: {self.model}")
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = None,
        max_tokens: int = None,
        stream: bool = False
    ) -> str | AsyncGenerator[str, None]:
        """Generate response from LLM using configured provider"""
        temperature = temperature or settings.LLM_TEMPERATURE
        max_tokens = max_tokens or settings.LLM_MAX_TOKENS
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            return await self.provider.generate(messages, temperature, max_tokens, stream)
        except Exception as e:
            logger.error(f"LLM generation failed with provider {self.provider_type}: {e}")
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
        await self.provider.close()


# Global LLM instance
llm = LLMWrapper()
