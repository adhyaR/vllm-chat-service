from fastapi import APIRouter, Depends, HTTPException
from vllm_chat_service.models.schemas import ChatRequest, ChatResponse
from vllm_chat_service.services.vllm_client import VLLMClient

router = APIRouter()


def get_vllm_client() -> VLLMClient:
    return VLLMClient()


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
        response = responses["choices"][0].message["content"]
        return ChatResponse(content=response, finish_reason=responses["finish_reason"])
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
