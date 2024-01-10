from abc import ABC, abstractmethod
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from models.pydantic.history import History, HistoryType
from models.pydantic.wallet import Wallet

class AbstractListWallets(ABC):

    @abstractmethod
    async def execute(self) -> list[Wallet]:
        raise NotImplementedError()

class AbstractGetWallet(ABC):

    @abstractmethod
    async def execute(self, wallet_id: int) -> Wallet:
        raise NotImplementedError()

class AbstractCreateWallet(ABC):

    @abstractmethod
    async def execute(self, name: str) -> Wallet:
        raise NotImplementedError()

class AbstractUpdateWallet(ABC):

    @abstractmethod
    async def execute(self, wallet_id: int, name: str) -> Wallet:
        raise NotImplementedError()

class AbstractDeleteWallet(ABC):

    @abstractmethod
    async def execute(self, wallet_id: int) -> None:
        raise NotImplementedError()