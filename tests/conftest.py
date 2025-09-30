import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from vllm_chat_service.main import app


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as async_client:
        yield async_client
