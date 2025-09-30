from fastapi import FastAPI
from vllm_chat_service.api.routes_health import router as health_router
from vllm_chat_service.api.routes_chat import router as chat_router

app = FastAPI(title="vLLM Chat Service API", version="1.0.0")
app.include_router(health_router, tags=["health"])
app.include_router(chat_router, tags=["chat"])


@app.get("/")
async def root():
    return {"message": "Welcome to the vLLM Chat Service API", "docs": "/docs"}
