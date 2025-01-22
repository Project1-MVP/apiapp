from sqlalchemy.orm import declarative_base
from core.config import settings
import asyncio
import asyncpg

engine = create_asyncpg_pool(settings.DATABASE_URL)
Base = declarative_base()

async def get_db():
    async with engine.begin() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e 

async def execute_transaction(query: str, *args):
    async with engine.begin() as session:
        try:
            await session.execute(query, *args)
        except Exception as e:
            await session.rollback()
            raise e
