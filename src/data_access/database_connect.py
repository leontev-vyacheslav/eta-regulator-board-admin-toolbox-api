import typing
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine("sqlite+aiosqlite:///data/data.sqlite3")
async_session_maker = async_sessionmaker(engine)

async def get_async_session() -> typing.AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

