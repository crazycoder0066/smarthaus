"""Request/response models for the API."""

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="The user's prompt.")
    thread_id: str | None = Field(
        default=None,
        description="Optional conversation id for multi-turn memory.",
    )


class ChatResponse(BaseModel):
    reply: str
    thread_id: str | None = None


class HealthResponse(BaseModel):
    status: str = "ok"
    app: str
    version: str

class ActionResult(BaseModel):
    pass
