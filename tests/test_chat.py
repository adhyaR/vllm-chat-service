import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_chat_mock(async_client: AsyncClient):
    response = await async_client.post(
        "/chat",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
        },
    )
    assert (
        response.status_code == 502
    )  # Since we don't have a real VLLM backend, we expect a 502 error
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_chat_rejects_bad_role(async_client: AsyncClient):
    response = await async_client.post(
        "/chat",
        json={
            "messages": [{"role": "invalid_role", "content": "Hello"}],
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_chat_rejects_negative_max_tokens(async_client: AsyncClient):
    response = await async_client.post(
        "/chat",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": -10,
        },
    )
    assert response.status_code == 422
