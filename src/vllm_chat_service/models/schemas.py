from pydantic import BaseModel, Field
from typing import List
from typing import Literal


class Message(BaseModel):
    role: Literal["user", "system", "assistant"] = Field(
        ..., description="Role of the message sender"
    )
    # TODO - enforce the roels at some point! and work on system afterwards
    content: str = Field(..., description="Content of the message")


class ChatRequest(BaseModel):
    # will use a default model for now and add model selection later
    messages: List[Message] = Field(
        ..., description="List of messages in the chat history"
    )
    max_tokens: int = Field(
        256, ge=1, description="Maximum number of tokens to generate in the response"
    )
    temperature: float = Field(
        0.7, ge=0, le=2, description="Sampling temperature for response generation"
    )


class ChatResponse(BaseModel):
    content: str = Field(..., description="Generated response content")
    finish_reason: str = Field(
        default="stop", description="Why generation stopped (e.g. stop, max length)"
    )  # or "length" if max tokens reached
