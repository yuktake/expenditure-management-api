from datetime import datetime
from sqlalchemy import (
    CheckConstraint,
    Enum,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from exceptions import AppException
from models import History, Wallet, HistoryType
from app.repositories.abstract_wallet_repository import AbstractWalletRepository

class WalletRepository(AbstractWalletRepository):
    async def add(self, session: AsyncSession, name: str) -> Wallet:
        wallet = WalletORM(name=name, histories=[])
        session.add(wallet)
        await session.flush()
        return wallet.to_entity()

    async def get_by_id(self,session: AsyncSession,wallet_id: int,) -> Wallet | None:
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

    async def get_all(self, session: AsyncSession) -> list[Wallet]:
        print("testttttttttttttttttttttttttttttt")
        stmt = select(WalletORM).options(
            selectinload(WalletORM.histories)
        )
        return [
            wallet.to_entity()
            for wallet in await session.scalars(
                stmt
            )
        ]

    async def add_history(
        self,
        session: AsyncSession,
        wallet_id: int,
        name: str,
        amount: int,
        type_: HistoryType,
        history_at: datetime,
    ) -> History:
        stmt = (
            select(WalletORM)
            .where(WalletORM.wallet_id == wallet_id)
            .options(
                selectinload(WalletORM.histories)
            )
        )
        wallet = await session.scalar(stmt)
        if not wallet:
            raise AppException()

        history = HistoryORM(
            name=name,
            amount=amount,
            type=type_,
            history_at=history_at,
            wallet_id=wallet.wallet_id,
        )
        wallet.histories.append(history)
        await session.flush()
        return history.to_entity()

    async def update(self, session: AsyncSession, wallet: Wallet) -> Wallet:
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

    async def delete(self, session: AsyncSession, wallet: Wallet) -> None:
        stmt = select(WalletORM).where(WalletORM.wallet_id == wallet.wallet_id)
        wallet_ = await session.scalar(stmt)
        if wallet_:
            await session.delete(wallet_)

    async def get_history_by_id(
        self,
        session: AsyncSession,
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

    async def update_history(self, session: AsyncSession, wallet_id: int, history: History) -> History:
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

    async def delete_history(self, session: AsyncSession, wallet_id: int, history: History):
        stmt = select(HistoryORM).where(
            HistoryORM.wallet_id == wallet_id,
            HistoryORM.history_id == history.history_id,
            )
        history_ = await session.scalar(stmt)
        if history_:
            await session.delete(history_)