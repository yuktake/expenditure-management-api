from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as ass
from dependencies.database import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from exceptions import AppException
from models import History, Wallet, HistoryType, UTCDatetime
from .abstract_wallet_repository import AbstractWalletRepository

from typing import AsyncIterator
from sqlalchemy.ext.asyncio import async_sessionmaker
from .wallet import (
    WalletORM,
    HistoryORM,
)

from dependencies.session import SessionInterface

from datetime import datetime

class TestWalletRepository(AbstractWalletRepository):

    async def add(self, session: ass, wallet: Wallet) -> Wallet:
        return Wallet(wallet_id=999, name="testing", histories=[])

    async def get_by_id(self, session: ass, wallet_id: int,) -> Wallet | None:
        return Wallet(
            wallet_id=999, 
            name="testing", 
            histories=[
                History(
                    history_id=999,
                    name="test_history",
                    amount=100,
                    type=HistoryType.INCOME,
                    history_at=datetime(2021, 12, 24, 3, 30, 20),
                    wallet_id=999,
                )
            ]
        )

    async def get_all(self, session: ass) -> list[Wallet]:
        return [
            Wallet(wallet_id=999, name="testing", histories=[]),
            Wallet(wallet_id=1000, name="testing2", histories=[])
        ]

    async def update(self, session: ass, wallet: Wallet) -> Wallet:
        return Wallet(wallet_id=wallet.wallet_id, name=wallet.name, histories=wallet.histories)

    async def delete(self, session: ass, wallet: Wallet) -> None:
        return None

    async def get_history_by_id(
        self,
        session: ass,
        wallet_id: int,
        history_id: int,
    ) -> History | None:
        return History(
            history_id=999,
            name="test_history",
            amount=100,
            type=HistoryType.INCOME,
            history_at=datetime(2021, 12, 24, 3, 30, 20),
            wallet_id=999,
        )

    async def add_history(
        self,
        session: ass,
        history: History
    ) -> History:
        return History(
            history_id=1,
            wallet_id=history.wallet_id,
            name=history.name,
            amount=999,
            type=history.type,
            history_at=history.history_at,
        )

    async def update_history(self, session: ass, wallet_id: int, history: History) -> History:
        return History(
            history_id=history.history_id,
            name=history.name,
            amount=history.amount,
            type=history.type,
            history_at=history.history_at,
            wallet_id=history.wallet_id,
        )

    async def delete_history(self, session: ass, wallet_id: int, history: History) -> None:
        return None