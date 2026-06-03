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

class CommandRequest(BaseModel):
    """A natural-language smart-home command, e.g. 'turn off the kitchen lights'."""

    text_command: str = Field(..., min_length=1, description="The command to run.")


class ToolCall(BaseModel):
    """One tool the agent invoked during a run."""

    name: str
    args: dict = Field(default_factory=dict)


class ActionResult(BaseModel):
    """The outcome of running a smart-home command through the agent."""

    reply: str  # the agent's final summary of what it changed
    tool_calls: list[ToolCall] = Field(default_factory=list)
