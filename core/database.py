from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from core.config import settings


engine:AsyncEngine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def execute_transaction(query: str, params: dict = None):
    async with engine.begin() as session:
        try:
            await session.execute(query, params)
        except Exception as e:
            await session.rollback()
            raise e

