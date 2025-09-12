from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import logging

from config import settings

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = create_async_engine(settings.get_async_db_url, echo=settings.app_debug)
async_session_maker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        print('Старт сесси БД')
        yield session
        print('Завершение сессии БД')