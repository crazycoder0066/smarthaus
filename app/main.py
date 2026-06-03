"""FastAPI application entrypoint for SmartHaus.

Run locally with:
    uvicorn app.main:app --reload
"""

import structlog
from fastapi import FastAPI

from app import __version__
from app.config import get_settings
from app.log_config import configure_logging
from app.schemas import ActionResult, HealthResponse

settings = get_settings()
configure_logging(level=settings.log_level, json_logs=settings.json_logs)
log = structlog.get_logger(__name__)

app = FastAPI(title=settings.app_name, version=__version__)


@app.get("/health", response_model=HealthResponse, tags=["system"])
async def health() -> HealthResponse:
    """Liveness probe — returns ok if the service is up."""
    return HealthResponse(status="ok", app=settings.app_name, version=__version__)

@app.post("/command", response_model=ActionResult)
async def command(body: dict):
    pass


if __name__ == "__main__":
    # Launch with:  python -m app.main   (run from the project root)
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
