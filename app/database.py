import logging
from typing import AsyncIterator
from sqlalchemy import Connection, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from exceptions import AppException
from models.alchemy.base import BaseORM
from config import Settings

logger = logging.getLogger(__name__)
settings = Settings()

async_engine = create_async_engine(
    settings.db_url,
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
)

async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield AsyncSessionLocal
    except SQLAlchemyError as e:
        logger.exception(e)
        raise AppException() from e

async def create_database_if_not_exist() -> None:
    def create_tables_if_not_exist(sync_conn: Connection,) -> None:
        if not inspect(sync_conn.engine).has_table("wallets"):
            BaseORM.metadata.create_all(
                sync_conn.engine
            )

    async with async_engine.connect() as conn:
        await conn.run_sync(
            create_tables_if_not_exist
        )