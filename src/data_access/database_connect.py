import os
import typing
from sys import platform
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy_utils import database_exists, create_database, drop_database


from src.data_models.user_data_model import UserDataModel
from src.data_models.regulator_device_data_model import RegulatorDeviceDataModel, BaseDataModel

env = os.environ.get('ENV')
is_production = env is not None and env == 'production'

if platform == 'windows':
    DATABASE_LOCALHOST = '172.21.120.224' # from wsl
else:
    DATABASE_LOCALHOST = 'localhost' # from docker (forwarded)

DB_PROVIDER = 'postgresql+psycopg:/'
DB_URL = f"{'database' if is_production else DATABASE_LOCALHOST}/eta_regulator_board_admin_toolbox"
DB_CONNECTION_STRING = f"{DB_PROVIDER}/postgres:1D#4wHm2@{DB_URL}"

async_engine = create_async_engine(DB_CONNECTION_STRING)
async_session_maker = async_sessionmaker(async_engine)

engine = create_engine(DB_CONNECTION_STRING)
session_maker = sessionmaker(engine)


async def get_async_session() -> typing.AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


def get_session() -> typing.Generator[Session, None, None]:
    session = session_maker()
    try:
        yield session
    finally:
        session.close()


def init_database():

    db_engine = create_engine(DB_CONNECTION_STRING)

    def init_data():
        SessionLocal = sessionmaker(db_engine)
        session = SessionLocal()

        session.add_all(
            [
                RegulatorDeviceDataModel(
                    id='54bc98fe-fb23-4971-a7a3-09cbae72aa64',
                    name='Omega-8F79',
                    mac_address='40:a3:6b:c9:8f:7a',
                    master_key='XAMhI3XWj+PaXP5nRQ+nNpEn9DKyHPTVa95i89UZL6o=',
                    creation_date='2024-02-06T12:32:06.553260',
                ),
                RegulatorDeviceDataModel(
                    id='9ee97d14-e299-4d41-83d7-200bbd7f02f5',
                    name='Omega-8F79-dev',
                    mac_address='02:42:ac:11:00:02',
                    master_key='XAMhI3XWj+PaXP5nRQ+nNpEn9DKyHPTVa95i89UZL6o=',
                    creation_date='2024-02-06T12:32:06.553260',
                ),
            ]
        )

        session.add_all(
            [
                UserDataModel(
                    id='c7bf8861-814d-466f-9118-e16640675aa9',
                    login='admin',
                    password='$2b$12$1zZ0YG2onw3Z0fg6wUywHe7gstOKYiNDsTUSPk9rcqbU/sUeqR/ni',
                )
            ]
        )

        session.commit()

    def init_schema():
        create_database(db_engine.url)
        BaseDataModel.metadata.create_all(db_engine)

    if is_production:
        if not database_exists(db_engine.url):
            init_schema()
            init_data()
    else:

        if database_exists(db_engine.url):
            drop_database(db_engine.url)

        init_schema()
        init_data()
