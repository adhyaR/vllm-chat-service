class VLLMClient:
    async def chat(self, payload: dict) -> dict:
        # Placeholder for actual vLLM interaction logic
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "This is a response from vLLM.",
                    }
                }
            ],
            "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
            "finish_reason": "stop",
        }
