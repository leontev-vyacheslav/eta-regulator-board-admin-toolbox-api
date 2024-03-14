import typing
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.utils.debugging import is_debug

DB_PROVIDER = 'sqlite+aiosqlite://'
DB_URL = 'data' if is_debug() else '_internal/data'
DB_FILE = 'data.sqlite3'

engine = create_async_engine(f'{DB_PROVIDER}/{DB_URL}/{DB_FILE}')
async_session_maker = async_sessionmaker(engine)


async def get_async_session() -> typing.AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
