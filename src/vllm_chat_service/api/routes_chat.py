from fastapi import APIRouter, Depends, HTTPException, Request
from vllm_chat_service.models.schemas import ChatRequest, ChatResponse
from vllm_chat_service.services.vllm_client import VLLMClient
import logging
import httpx

log = logging.getLogger(__name__)
router = APIRouter()


def get_vllm_client(request: Request) -> VLLMClient:
    """Retrieve the vLLM client from the app state.

    Args:
        request: A FastAPI Request object.
    Returns:
        An instance of VLLMClient."""
    return request.app.state.vllm_client


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest, vllm_client: VLLMClient = Depends(get_vllm_client)
) -> ChatResponse:
    try:  # we call on a mock for now and add the httpx call later
        responses = await vllm_client.chat(
            {
                "model": "placeholder-model",
                "messages": [m.model_dump() for m in request.messages],
                "max_tokens": request.max_tokens,
                "temperature": request.temperature,
                "stream": False,
            }
        )  # have multiple response options (hopefully)
        response = responses["choices"][0]
        return ChatResponse(
            content=response["message"]["content"],
            finish_reason=response.get("finish_reason", "stop"),
        )
    except httpx.HTTPError as e:
        log.error(f"VLLM upstream error {e}")
        raise HTTPException(status_code=502, detail="VLLM is unavailable")
