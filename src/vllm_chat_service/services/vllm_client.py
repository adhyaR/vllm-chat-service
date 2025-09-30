import httpx
from vllm_chat_service.core.config import settings


class VLLMClient:
    def __init__(self, base_url: str | None = None):
        self._client = httpx.AsyncClient(
            base_url=base_url or settings.VLLM_URL, timeout=30
        )

    async def chat(self, payload: dict) -> dict:
        # Placeholder for actual vLLM interaction logic
        body = {
            "model": settings.MODEL_ID,
            "messages": payload.get("messages", []),
            "max_tokens": payload.get("max_tokens", 256),
            "temperature": payload.get("temperature", 1.0),
            "stream": payload.get("stream", False),
        }
        request = await self._client.post("/chat/completions", json=body)
        request.raise_for_status()
        return request.json()
