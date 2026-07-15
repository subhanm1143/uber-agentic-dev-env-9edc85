"""Domain errors that each carry an HTTP status, plus a JSON handler."""
from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse


class ApiError(Exception):
    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


class NotFound(ApiError):
    def __init__(self, message: str = "not found") -> None:
        super().__init__(404, message)


async def api_error_handler(_request: Request, exc: ApiError) -> JSONResponse:
    return JSONResponse(status_code=exc.status, content={"error": exc.message})
