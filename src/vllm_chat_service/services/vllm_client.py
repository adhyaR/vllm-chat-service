import httpx
from vllm_chat_service.core.config import settings


class VLLMClient:
    """Client to interact with vLLM's chat completion endpoint.

    This client handles the HTTP communication with a vLLM backend server, sends chat requests and parses responses.
    """

    def __init__(self, base_url: str | None = None):
        """initialise the vLLM client

        Args:
            base_url: Base URL for vLLM API. If None, uses the URL from settings.
        """
        self._client = httpx.AsyncClient(
            base_url=base_url or settings.VLLM_URL, timeout=30
        )

    async def chat(self, payload: dict) -> dict:
        """Send a chat request to the vLLM backend and return the response.

        Args:
            payload: A dictionary containing the chat request parameters.
        Returns:
            A dictionary containing the chat response from vLLM.
        Raises:
            httpx.HTTPError: If the request to the vLLM backend fails."""
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
