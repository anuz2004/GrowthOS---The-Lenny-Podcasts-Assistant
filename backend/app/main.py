from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings
from app.core.logger import logger
from app.lifespan import lifespan
from app.core.error_handlers import register_error_handlers


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="GrowthOS Backend API",
    lifespan=lifespan,
)
register_error_handlers(app)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://growthos-frontend-five.vercel.app/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all API routes
app.include_router(api_router)


@app.get(
    "/",
    tags=["Root"],
    summary="Health Check",
)
async def root():
    logger.info("Root endpoint called")

    return {
        "success": True,
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
    }