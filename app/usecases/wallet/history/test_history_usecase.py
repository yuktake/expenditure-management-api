from datetime import datetime

from dependencies.repository import WalletRepositoryInterface
from dependencies.session import SessionInterface

from exceptions import NotFound
from models.pydantic.history import History, HistoryType
from .abstract_history_usecase import(
    AbstractListHistories,
    AbstractGetHistory,
    AbstractCreateHistory,
    AbstractUpdateHistory,
    AbstractDeleteHistory,
    AbstractMoveHistory,
)

class ListHistories(AbstractListHistories):
    def __init__(
        self,
        session: SessionInterface,
        repo: WalletRepositoryInterface,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(self, wallet_id: int) -> list[History]:
        print("testing")
        sess = self.session.get_session()
        async with sess() as s:
            wallet = await self.repo.get_by_id(s, wallet_id)
            if not wallet:
                raise NotFound("wallet", wallet_id)

        return wallet.histories

class GetHistory(AbstractGetHistory):
    def __init__(
        self,
        session: SessionInterface,
        repo: WalletRepositoryInterface,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self,
        wallet_id: int,
        history_id: int,
    ) -> History:
        print("testing")
        sess = self.session.get_session()
        async with sess() as s:
            history = await self.repo.get_history_by_id(s, wallet_id, history_id)
            if not history:
                raise NotFound("history", history_id)

        return history

class CreateHistory(AbstractCreateHistory):
    def __init__(
        self,
        session: SessionInterface,
        repo: WalletRepositoryInterface,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self,
        wallet_id: int,
        name: str,
        amount: int,
        type_: HistoryType,
        history_at: datetime,
    ) -> History:
        print("testing")
        history = History(
            history_id = None,
            wallet_id = wallet_id,
            name = name,
            amount = amount,
            type = type_,
            history_at = history_at
        )
        sess = self.session.get_session()
        async with sess.begin() as s:
            wallet = await self.repo.get_by_id(s, history.wallet_id)
            if not wallet:
                raise NotFound("wallet", history.wallet_id)

            created_history = await self.repo.add_history(
                s,
                history
            )
        return created_history

class UpdateHistory(AbstractUpdateHistory):
    def __init__(
        self,
        session: SessionInterface,
        repo: WalletRepositoryInterface,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self,
        wallet_id: int,
        history_id: int,
        name: str,
        amount: int,
        type_: HistoryType,
        history_at: datetime,
    ) -> History:
        print("testing")
        sess = self.session.get_session()
        async with sess.begin() as s:
            history = await self.repo.get_history_by_id(s, wallet_id, history_id)
            if not history:
                raise NotFound("history", history_id)

            update_history = History(
                history_id = history_id,
                wallet_id = wallet_id,
                name = name,
                amount = amount,
                type = type_,
                history_at = history_at
            )
            await self.repo.update_history(s, wallet_id, update_history)
        return update_history

class DeleteHistory(AbstractDeleteHistory):
    def __init__(
        self,
        session: SessionInterface,
        repo: WalletRepositoryInterface,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self, wallet_id: int, history_id: int
    ) -> None:
        print("testing")
        sess = self.session.get_session()
        async with sess.begin() as s:
            history = await self.repo.get_history_by_id(s, wallet_id, history_id)
            if history:
                await self.repo.delete_history(s, history.wallet_id, history)

class MoveHistory(AbstractMoveHistory):
    def __init__(
        self,
        session: SessionInterface,
        repo: WalletRepositoryInterface,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self,
        wallet_id: int,
        history_id: int,
        destination_id: int
    ) -> History:
        print("testing")
        sess = self.session.get_session()
        async with sess.begin() as s:
            history = await self.repo.get_history_by_id(s, wallet_id, history_id)
            if not history:
                raise NotFound("history", history_id)

            wallet = await self.repo.get_by_id(s, destination_id)
            if not wallet:
                raise NotFound("wallet", wallet_id)

            move_history = History(
                history_id = history.history_id,
                wallet_id = wallet.wallet_id,
                name = history.name,
                amount = history.amount,
                type = history.type,
                history_at = history.history_at
            )
            await self.repo.update_history(s, wallet_id, move_history)

        return move_history