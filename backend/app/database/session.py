from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

DATABASE_URL = settings.database_url.replace(
    "postgresql://",
    "postgresql+asyncpg://",
    1,
)

engine = create_async_engine(
    DATABASE_URL,
    echo=settings.debug,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)