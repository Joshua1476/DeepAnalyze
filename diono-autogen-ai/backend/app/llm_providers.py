"""
Multi-provider LLM support
Supports OpenAI, Anthropic, Google Gemini, Hugging Face, Ollama, Qwen, DeepSeek
"""
from typing import Optional, Dict, Any, AsyncGenerator
import httpx
import json
from loguru import logger
from .config import settings


class BaseLLMProvider:
    """Base class for LLM providers"""
    
    def __init__(self, api_url: str, api_key: Optional[str] = None):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=300.0)
    
    async def generate(
        self,
        messages: list,
        temperature: float,
        max_tokens: int,
        stream: bool = False
    ) -> str | AsyncGenerator[str, None]:
        """Generate response - to be implemented by subclasses"""
        raise NotImplementedError
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


class OpenAIProvider(BaseLLMProvider):
    """OpenAI and OpenAI-compatible providers (OpenRouter, Together, Groq, etc.)"""
    
    async def generate(self, messages: list, temperature: float, max_tokens: int, stream: bool = False):
        payload = {
            "model": settings.LLM_MODEL,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        if stream:
            return self._stream_response(payload, headers)
        else:
            response = await self.client.post(
                f"{self.api_url}/v1/chat/completions",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
    
    async def _stream_response(self, payload: dict, headers: dict):
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


class OllamaProvider(BaseLLMProvider):
    """Ollama local LLM provider"""
    
    async def generate(self, messages: list, temperature: float, max_tokens: int, stream: bool = False):
        # Ollama uses /api/chat endpoint
        payload = {
            "model": settings.LLM_MODEL,
            "messages": messages,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            },
            "stream": stream
        }
        
        if stream:
            return self._stream_response(payload)
        else:
            response = await self.client.post(
                f"{self.api_url}/api/chat",
                json=payload
            )
            response.raise_for_status()
            result = response.json()
            return result["message"]["content"]
    
    async def _stream_response(self, payload: dict):
        async with self.client.stream(
            "POST",
            f"{self.api_url}/api/chat",
            json=payload
        ) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                try:
                    chunk = json.loads(line)
                    if "message" in chunk and "content" in chunk["message"]:
                        yield chunk["message"]["content"]
                    if chunk.get("done", False):
                        break
                except json.JSONDecodeError:
                    continue


class GeminiProvider(BaseLLMProvider):
    """Google Gemini provider"""
    
    async def generate(self, messages: list, temperature: float, max_tokens: int, stream: bool = False):
        # Convert messages to Gemini format
        contents = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }
        
        url = f"{self.api_url}/v1/models/{settings.LLM_MODEL}:generateContent"
        if self.api_key:
            url += f"?key={self.api_key}"
        
        if stream:
            url = url.replace(":generateContent", ":streamGenerateContent")
            return self._stream_response(payload, url)
        else:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]
    
    async def _stream_response(self, payload: dict, url: str):
        async with self.client.stream("POST", url, json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                try:
                    chunk = json.loads(line)
                    if "candidates" in chunk:
                        text = chunk["candidates"][0]["content"]["parts"][0]["text"]
                        yield text
                except json.JSONDecodeError:
                    continue


class HuggingFaceProvider(BaseLLMProvider):
    """Hugging Face Inference API provider"""
    
    async def generate(self, messages: list, temperature: float, max_tokens: int, stream: bool = False):
        # Convert messages to prompt
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": temperature,
                "max_new_tokens": max_tokens,
                "return_full_text": False
            }
        }
        
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        response = await self.client.post(
            f"{self.api_url}/models/{settings.LLM_MODEL}",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            return result[0].get("generated_text", "")
        return str(result)


class QwenProvider(BaseLLMProvider):
    """Qwen (Alibaba Cloud) provider - OpenAI-compatible"""
    
    async def generate(self, messages: list, temperature: float, max_tokens: int, stream: bool = False):
        # Qwen uses OpenAI-compatible API
        openai_provider = OpenAIProvider(self.api_url, self.api_key)
        return await openai_provider.generate(messages, temperature, max_tokens, stream)


class DeepSeekProvider(BaseLLMProvider):
    """DeepSeek provider - OpenAI-compatible"""
    
    async def generate(self, messages: list, temperature: float, max_tokens: int, stream: bool = False):
        # DeepSeek uses OpenAI-compatible API
        openai_provider = OpenAIProvider(self.api_url, self.api_key)
        return await openai_provider.generate(messages, temperature, max_tokens, stream)


def get_provider(provider_type: str, api_url: str, api_key: Optional[str] = None) -> BaseLLMProvider:
    """Factory function to get the appropriate provider"""
    providers = {
        "openai": OpenAIProvider,
        "ollama": OllamaProvider,
        "gemini": GeminiProvider,
        "huggingface": HuggingFaceProvider,
        "qwen": QwenProvider,
        "deepseek": DeepSeekProvider,
        "anthropic": OpenAIProvider,  # Anthropic is OpenAI-compatible
        "groq": OpenAIProvider,  # Groq is OpenAI-compatible
        "together": OpenAIProvider,  # Together is OpenAI-compatible
        "openrouter": OpenAIProvider,  # OpenRouter is OpenAI-compatible
    }
    
    provider_class = providers.get(provider_type.lower(), OpenAIProvider)
    return provider_class(api_url, api_key)
