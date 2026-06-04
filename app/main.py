"""FastAPI application entrypoint for SmartHaus.

Run locally with:
    uvicorn app.main:app --reload
"""

from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field
import structlog
from fastapi import FastAPI, Query

from app import __version__, world
from app.agent import run_command
from app.config import get_settings
from app.log_config import configure_logging
from app.schemas import ActionResult, CommandRequest, HealthResponse

class Item(BaseModel):
    id: int
    description: str

class ItemFilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    skip: int = Field(100, gt=0, le=100)

settings = get_settings()
configure_logging(level=settings.log_level, json_logs=settings.json_logs)
log = structlog.get_logger(__name__)

app = FastAPI(title=settings.app_name, version=__version__)

mock_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/health", response_model=HealthResponse, tags=["system"])
async def health() -> HealthResponse:
    """Liveness probe — returns ok if the service is up."""
    return HealthResponse(status="ok", app=settings.app_name, version=__version__)

@app.get("/world", tags=["world"])
async def world_status() -> dict:
    """Return the current state of every device and sensor."""
    return {"devices": world.WORLD, "sensors": world.SENSORS}


@app.get('/items')
async def items(filterQuery: Annotated[ItemFilterParams, Query()]):
    skip = filterQuery.skip
    limit = filterQuery.limit
    return mock_items_db[skip:skip+limit]


@app.post('/items')
async def items(item: Item):
    return item


@app.post("/command", response_model=ActionResult)
async def command(body: CommandRequest) -> ActionResult:
    return await run_command(body.text_command)


if __name__ == "__main__":
    # Launch with:  python -m app.main   (run from the project root)
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
