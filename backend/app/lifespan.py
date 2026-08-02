from contextlib import asynccontextmanager

from app.core.logger import logger
from app.database.connection import check_database_connection


@asynccontextmanager
async def lifespan(app):
    logger.info("GrowthOS API Started")

    try:
        await check_database_connection()
        logger.success("Connected to Supabase")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")

    yield

    logger.info("GrowthOS API Shutdown")