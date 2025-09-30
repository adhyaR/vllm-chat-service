# vllm-chat-service
A FastAPI-based chat service that provides a clean API Gateway to vLLM.

## Overview
This service wraps vLLM's chat completion API with:
- Request validation using Pydantic schemas
- Structured error handling with appropriate HTTP status codes
- Dependency injections for testability
- Comprehensive test coverage
- Environment-based configuration

## Requirements
- Python 3.11+
- GPU with CUDA Support (CPU can be used to serve models, but is much slower)
- [uv](https://github.com/astral-sh/uv) for dependency management
- vLLM version 0.10.2+

**Note**: for WSL users, GPU memory detection can be suboptimal. Use '--gpu-memory-utilization 0.7' to avoid memory issues.

For CPU Users, use '--device cpu' instead of the above when using the vLLM backend.

## Setup
1. **Clone and install dependencies**:
```bash
   git clone https://github.com/adhyaR/vllm-chat-service.git
   cd vllm-chat-service
   uv sync --dev
```
2. **Configure environments**:
```cp .env.example .env```
Note: edit .env if you need to change defaults e.g. model.

Currently, the model has been set as TinyLlama/TinyLlama-1.1B-Chat-v1.0

3. **Start vLLM backend**:
For GPU users:
```vllm serve TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
     --port 8000 \
     --gpu-memory-utilization 0.7
```
For CPU users:
```vllm serve TinyLlama/TinyLlama-1.1B-Chat-v1.0 \
     --port 8000 \
     --device cpu
```

The model in the commands above here can be replaced with any of the models supported by vLLM (https://docs.vllm.ai/en/v0.9.2/features/reasoning_outputs.html#supported-models).

4. In a new terminal, start the API Service:
```uv run unicorn vllm_chat_service.main:app --host 0.0.0.0 --port 8001
```
## Usage
**Chat Completion**
Send a chat request
```
curl -X POST http://127.0.0.1:8001/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello, how are you?"}],
    "max_tokens": 50,
    "temperature": 0.7
  }'
```

Response:
```{
  "content": "I am well, thank you. How about you?",
  "finish_reason": "stop"
}
```

Health check:
```curl http://127.0.0.1:8001/health```

## API Documentation
Once running, you can visit the following:
- Swagger UI: http://127.0.0.1:8001/docs
- ReDoc: http://127.0.0.1:8001/redoc

## Environment Variable Configuration
| Variable | Default | Description |
| --- | --- | --- |
| VLLM_URL | http://127.0.0/1:8001/v1 | vLLM API's base URL |
| MODEL_ID | TinyLlama/TinyLlama-1.1B-Chat-v1.0 | Model identifier (for reference) |
| LOG_LEVEL | INFO | Logging level (DEBUG, INFO, WARNING, ERROR) |

## Testing
To run the test suite, run:
```uv run pytest -v```
To run tests quietly:
```uv run pytest -q```

Note that the existing tests use mocked vLLM clients, so you don't need a running vLLM instance to run tests.

## Project Structure
vllm-chat-service/
├── src/vllm_chat_service/
│   ├── api/
│   │   ├── routes_chat.py       # Chat endpoint with error handling
│   │   └── routes_health.py     # Health check endpoint
│   ├── core/
│   │   ├── config.py            # Pydantic settings management
│   │   └── logging.py           # Logging configuration
│   ├── models/
│   │   └── schemas.py           # Request/response model schemas
│   ├── services/
│   │   └── vllm_client.py       # vLLM API client
│   ├── __init__.py
│   └── main.py                  # FastAPI application
├── tests/
│   ├── conftest.py              # Test fixtures
│   ├── test_chat.py             # Chat endpoint tests
│   ├── test_health.py           # Health check tests
│   └── test_sanity.py           # Basic sanity tests
├── .env                         # Environment configuration (not committed)
├── .env.example                 # Example environment file
├── pyproject.toml               # Project dependencies and config
└── README.md                    # This document

## Design Decisions
**Dependency injection**: The VLLMClient attached to app.state during startup and is injected via FastAPI's dependency stream. This enables ease of testing, as we can mock the client in tests.
**Error Handling**: Network errors from vLLM are caught and returned as ```502 Bad Gateway``` with a clear error message. This distinguishes between client errors which are 4__ and upstream vLLM service issues (5__).
**Validation**: Pydantic models validate all their inputs automatically. Invalid roles, negative *max_tokens* and incorrectly formed requests are rejected with ```422 Unprocessable Entity``` before reaching the remaining logic.
**Testing strategy***: This is touched on earlier. Tests stub the vLLM client rather than requiring a vLLM instance. This makes CI/CD faster and more reliable, whilst still testing the service's logic, validation and error handling.

## Limitations and Future Work
**Basic Health Check**: The ```health``` endpoint only checks if the service is running, but a checker for vLLM would be more robust.
**Single Model**: The service currently forwards requests to a single vLLM instance. Multi-model support or model routing could be added.
***Limited observability**: Structured logging, metrics and tracing would improve production readiness.

## Development
To install with dev dependencies:
```uv sync --dev```

Run with auto-reload for development:
```uv run uvicorn vllm_chat_service.main:app --reload --port 8001```
