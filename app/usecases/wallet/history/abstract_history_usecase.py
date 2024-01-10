from datetime import datetime
from abc import ABC, abstractmethod

from models.pydantic.history import History, HistoryType

class AbstractListHistories:

    @abstractmethod
    async def execute(self, wallet_id: int) -> list[History]:
        raise NotImplementedError()

class AbstractGetHistory:

    @abstractmethod
    async def execute(
        self,
        wallet_id: int,
        history_id: int,
    ) -> History:
        raise NotImplementedError()

class AbstractCreateHistory:

    @abstractmethod
    async def execute(
        self,
        wallet_id: int,
        name: str,
        amount: int,
        type_: HistoryType,
        history_at: datetime,
    ) -> History:
        raise NotImplementedError()

class AbstractUpdateHistory:

    @abstractmethod
    async def execute(
        self,
        wallet_id: int,
        history_id: int,
        name: str,
        amount: int,
        type_: HistoryType,
        history_at: datetime,
    ) -> History:
        raise NotImplementedError()

class AbstractDeleteHistory:

    @abstractmethod
    async def execute(
        self, 
        wallet_id: int, 
        history_id: int
    ) -> None:
        raise NotImplementedError()

class AbstractMoveHistory:

    @abstractmethod
    async def execute(
        self,
        wallet_id: int,
        history_id: int,
        destination_id: int
    ) -> History:
        raise NotImplementedError()