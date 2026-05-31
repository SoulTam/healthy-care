from __future__ import annotations

import json
import logging
import time
from typing import Any, AsyncGenerator

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        api_key: str | None = None,
        timeout: int = 60,
        max_retries: int = 3,
    ):
        self.base_url = (base_url or settings.LLM_BASE_URL).rstrip("/")
        self.model = model or settings.LLM_MODEL or "qwen2.5:7b"
        self.api_key = api_key or settings.LLM_API_KEY
        self.timeout = timeout
        self.max_retries = max_retries
        self._available = False

    async def check_availability(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                resp = await client.get(f"{self.base_url}/api/tags")
                self._available = resp.status_code == 200
        except Exception as e:
            logger.warning(f"LLM service unavailable at {self.base_url}: {e}")
            self._available = False
        return self._available

    @property
    def available(self) -> bool:
        return self._available

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        if not self._available:
            return self._fallback_response(prompt)

        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }
        if system_prompt:
            payload["system"] = system_prompt

        last_error = None
        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    resp = await client.post(
                        f"{self.base_url}/api/generate",
                        json=payload,
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    return data.get("response", "")
            except Exception as e:
                last_error = e
                logger.warning(
                    f"LLM generate attempt {attempt + 1} failed: {e}"
                )
                if attempt < self.max_retries - 1:
                    time.sleep(2**attempt)

        logger.error(f"LLM generate failed after {self.max_retries} retries: {last_error}")
        return self._fallback_response(prompt)

    async def generate_stream(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> AsyncGenerator[str, None]:
        if not self._available:
            yield self._fallback_response(prompt)
            return

        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }
        if system_prompt:
            payload["system"] = system_prompt

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST", f"{self.base_url}/api/generate", json=payload
                ) as resp:
                    async for line in resp.aiter_lines():
                        if line.strip():
                            try:
                                chunk = json.loads(line)
                                if chunk.get("response"):
                                    yield chunk["response"]
                                if chunk.get("done"):
                                    return
                            except json.JSONDecodeError:
                                continue
        except Exception as e:
            logger.error(f"LLM stream error: {e}")
            yield self._fallback_response(prompt)

    async def chat(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        if not self._available:
            return self._fallback_response(str(messages))

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                )
                resp.raise_for_status()
                data = resp.json()
                return data.get("message", {}).get("content", "")
        except Exception as e:
            logger.error(f"LLM chat error: {e}")
            return self._fallback_response(str(messages))

    def _fallback_response(self, prompt: str) -> str:
        return ""


llm_client = LLMClient()
