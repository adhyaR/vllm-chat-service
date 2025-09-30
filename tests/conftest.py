import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from vllm_chat_service.main import app
from vllm_chat_service.services.vllm_client import VLLMClient


@pytest_asyncio.fixture
async def async_client():
    app.state.vllm_client = VLLMClient()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as async_client:
        yield async_client
    await app.state.vllm_client._client.aclose()
