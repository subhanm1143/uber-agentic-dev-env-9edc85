"""The FastAPI app: mounts routers and the error handler."""
from fastapi import FastAPI

from .api.errors import ApiError, api_error_handler
from .api.routes import projects, runs, tasks


def create_app() -> FastAPI:
    app = FastAPI(title="Agentic Orchestrator")

    app.add_exception_handler(ApiError, api_error_handler)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    app.include_router(projects.router)
    app.include_router(tasks.router)
    app.include_router(runs.router)
    return app


app = create_app()
