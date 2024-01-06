from abc import ABC, abstractmethod
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from models.history import History, HistoryType
from models.wallet import Wallet

class AbstractWalletRepository(ABC):

    @abstractmethod
    async def add(self, session: AsyncSession, name: str) -> Wallet:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self,session: AsyncSession,wallet_id: int,) -> Wallet | None:
        raise NotImplementedError()

    @abstractmethod
    async def get_all(self, session: AsyncSession) -> list[Wallet]:
        raise NotImplementedError()

    @abstractmethod
    async def add_history(self,session: AsyncSession,wallet_id: int,name: str,amount: int,type_: HistoryType,history_at: datetime,) -> History:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, session: AsyncSession, wallet: Wallet) -> Wallet:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, session: AsyncSession, wallet: Wallet) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_history_by_id(self,session: AsyncSession,wallet_id: int,history_id: int,) -> History | None:
        raise NotImplementedError()

    @abstractmethod
    async def update_history(self, session: AsyncSession, wallet_id: int, history: History) -> History:
        raise NotImplementedError()

    @abstractmethod
    async def delete_history(self, session: AsyncSession, wallet_id: int, history: History):
        raise NotImplementedError()