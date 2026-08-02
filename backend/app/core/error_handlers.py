from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import GrowthOSError


def register_error_handlers(app: FastAPI):

    @app.exception_handler(GrowthOSError)
    async def growthos_exception_handler(
        request: Request,
        exc: GrowthOSError,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "title": exc.title,
                    "message": exc.message,
                    "suggestions": exc.suggestions,
                    "technical": exc.technical,
                    "status_code": exc.status_code,
                }
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ):
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "title": "Unexpected Error",
                    "message": "Something unexpected happened while processing your request.",
                    "suggestions": [
                        "Try again.",
                        "Refresh the page.",
                        "If the problem persists, check the backend logs.",
                    ],
                    "technical": str(exc),
                    "status_code": 500,
                }
            },
        )