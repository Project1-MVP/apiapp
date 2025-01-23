from sqlalchemy.orm import declarative_base
from core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

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
