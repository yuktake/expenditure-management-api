from dependencies.repository import WalletRepositoryInterface
from dependencies.session import SessionInterface

from exceptions import NotFound
from models.pydantic.wallet import Wallet
from .abstract_wallet_usecase import(
    AbstractListWallets,
    AbstractGetWallet,
    AbstractCreateWallet,
    AbstractUpdateWallet,
    AbstractDeleteWallet,
)

class ListWallets(AbstractListWallets):

    def __init__(
        self,
        session: SessionInterface,
        repo: WalletRepositoryInterface,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(self) -> list[Wallet]:
        sess = self.session.get_session()
        async with sess() as s:
            wallets = await self.repo.get_all(s)
        return wallets

class GetWallet(AbstractGetWallet):
    def __init__(
        self,
        session: SessionInterface,
        repo: WalletRepositoryInterface,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self, wallet_id: int,
    ) -> Wallet:
        sess = self.session.get_session()
        async with sess() as s:
            wallet = await self.repo.get_by_id(s, wallet_id)
            if not wallet:
                raise NotFound("wallet", wallet_id)
        return wallet

class CreateWallet(AbstractCreateWallet):
    def __init__(
        self,
        session: SessionInterface,
        repo: WalletRepositoryInterface,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(self, name: str) -> Wallet:
        wallet = Wallet(wallet_id=None, name=name, histories=[])
        sess = self.session.get_session()
        # INSERT/UPDATE/DELETE などはトランザクションのためbegin()が必要
        async with sess.begin() as s:
            created_wallet = await self.repo.add(s, wallet=wallet)

        return created_wallet

class UpdateWallet(AbstractUpdateWallet):
    def __init__(
        self,
        session: SessionInterface,
        repo: WalletRepositoryInterface,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self, wallet_id: int, name: str
    ) -> Wallet:
        sess = self.session.get_session()
        async with sess.begin() as s:
            wallet = await self.repo.get_by_id(s, wallet_id)

            if not wallet:
                raise NotFound("wallet", wallet_id)
            update_wallet = Wallet(
                wallet_id=wallet.wallet_id,
                name=name,
                histories=wallet.histories,
            )
            await self.repo.update(s, update_wallet)

        return update_wallet

class DeleteWallet(AbstractDeleteWallet):
    def __init__(
        self,
        session: SessionInterface,
        repo: WalletRepositoryInterface,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self, wallet_id: int
    ) -> None:
        sess = self.session.get_session()
        async with sess.begin() as s:
            wallet = await self.repo.get_by_id(s, wallet_id)
            if wallet:
                await self.repo.delete(s, wallet)