from fastapi import FastAPI
from vllm_chat_service.api.routes_health import router as health_router
from vllm_chat_service.api.routes_chat import router as chat_router
from vllm_chat_service.core.logging import configure_logging
from vllm_chat_service.core.config import settings
from vllm_chat_service.services.vllm_client import VLLMClient

configure_logging(settings.LOG_LEVEL)

app = FastAPI(title="vLLM Chat Service API", version="1.0.0")
app.include_router(health_router, tags=["health"])
app.include_router(chat_router, tags=["chat"])


@app.get("/")
async def root():
    return {"message": "Welcome to the vLLM Chat Service API", "docs": "/docs"}


@app.on_event("startup")
async def startup_event():
    app.state.vllm_client = VLLMClient()


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.vllm_client._client.aclose()
