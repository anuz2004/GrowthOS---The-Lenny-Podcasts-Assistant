from app.database.session import engine


async def check_database_connection():
    async with engine.begin() as conn:
        await conn.run_sync(lambda _: None)