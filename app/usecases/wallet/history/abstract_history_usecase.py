from datetime import datetime
from abc import ABC, abstractmethod

from models.pydantic.history import History, HistoryType

class AbstractListHistories(ABC):

    @abstractmethod
    async def execute(self, wallet_id: int) -> list[History]:
        raise NotImplementedError()

class AbstractGetHistory(ABC):

    @abstractmethod
    async def execute(
        self,
        wallet_id: int,
        history_id: int,
    ) -> History:
        raise NotImplementedError()

class AbstractCreateHistory(ABC):

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

class AbstractUpdateHistory(ABC):

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

class AbstractDeleteHistory(ABC):

    @abstractmethod
    async def execute(
        self, 
        wallet_id: int, 
        history_id: int
    ) -> None:
        raise NotImplementedError()

class AbstractMoveHistory(ABC):

    @abstractmethod
    async def execute(
        self,
        wallet_id: int,
        history_id: int,
        destination_id: int
    ) -> History:
        raise NotImplementedError()