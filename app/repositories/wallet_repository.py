from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as ass
from dependencies.database import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from exceptions import AppException
from models.pydantic.history import History, HistoryType
from models.pydantic.wallet import Wallet
from .abstract_wallet_repository import AbstractWalletRepository

from typing import AsyncIterator
from sqlalchemy.ext.asyncio import async_sessionmaker
from models.alchemy.wallet import WalletORM
from models.alchemy.history import HistoryORM

from dependencies.session import SessionInterface

class WalletRepository(AbstractWalletRepository):

    async def add(self, session: ass, wallet: Wallet) -> Wallet:
        wallet_orm = WalletORM(name=wallet.name, histories=[])
        session.add(wallet_orm)
        await session.flush()
        return wallet_orm.to_entity()

    async def get_by_id(self, session: ass, wallet_id: int,) -> Wallet | None:
        stmt = (
            select(WalletORM)
            .where(WalletORM.wallet_id == wallet_id)
            .options(
                selectinload(WalletORM.histories)
            )
        )
        wallet = await session.scalar(stmt)
        if not wallet:
            return None
        return wallet.to_entity()

    async def get_all(self, session: ass) -> list[Wallet]:
        stmt = select(WalletORM).options(
            selectinload(WalletORM.histories)
        )
        
        return [
            wallet.to_entity() for wallet in await session.scalars(stmt)
        ]

    async def update(self, session: ass, wallet: Wallet) -> Wallet:
        stmt = (
            select(WalletORM)
            .where(WalletORM.wallet_id == wallet.wallet_id)
            .options(selectinload(WalletORM.histories))
        )
        wallet_ = await session.scalar(stmt)
        if not wallet_:
            raise AppException()

        wallet_.update(wallet, wallet_.histories)
        await session.flush()
        return wallet_.to_entity()

    async def delete(self, session: ass, wallet: Wallet) -> None:
        stmt = select(WalletORM).where(WalletORM.wallet_id == wallet.wallet_id)
        wallet_ = await session.scalar(stmt)
        if wallet_:
            await session.delete(wallet_)

    async def get_history_by_id(
        self,
        session: ass,
        wallet_id: int,
        history_id: int,
    ) -> History | None:
        stmt = (
            select(HistoryORM)
            .where(
                HistoryORM.wallet_id == wallet_id, HistoryORM.history_id == history_id
            )
            .options(joinedload(HistoryORM.wallet))
        )
        history_ = await session.scalar(stmt)
        if not history_:
            return None

        return history_.to_entity()

    async def add_history(
        self,
        session: ass,
        history: History
    ) -> History:
        stmt = (
            select(WalletORM)
            .where(WalletORM.wallet_id == history.wallet_id)
            .options(
                selectinload(WalletORM.histories)
            )
        )
        wallet = await session.scalar(stmt)
        if not wallet:
            raise AppException()

        history_orm = HistoryORM(
            name=history.name,
            amount=history.amount,
            type=history.type,
            history_at=history.history_at,
            wallet_id=wallet.wallet_id,
        )
        wallet.histories.append(history_orm)
        await session.flush()
        return history_orm.to_entity()

    async def update_history(self, session: ass, wallet_id: int, history: History) -> History:
        stmt = select(HistoryORM).where(
            HistoryORM.wallet_id == wallet_id,
            HistoryORM.history_id == history.history_id,
            )
        history_ = await session.scalar(stmt)
        if not history_:
            raise AppException()

        history_.update(history)
        await session.flush()
        return history_.to_entity()

    async def delete_history(self, session: ass, wallet_id: int, history: History) -> None:
        stmt = select(HistoryORM).where(
            HistoryORM.wallet_id == wallet_id,
            HistoryORM.history_id == history.history_id,
            )
        history_ = await session.scalar(stmt)
        if history_:
            await session.delete(history_)