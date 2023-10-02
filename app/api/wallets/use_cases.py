from db.database import (
    AsyncSession,
)
from db.database import WalletRepository
from exceptions import NotFound
from models import Wallet

from typing import  AsyncIterator
from sqlalchemy.ext.asyncio import async_sessionmaker

# class Test:
#     def __init__(self, config) -> None:
#         print("ccccccccccccccccccccccccccc")
#         # print(config.app_name)
#         print(config.aaa)

class ListWallets:

    def __init__(
        self,
        session: AsyncSession,
        repo: WalletRepository,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(self) -> list[Wallet]:
        async with self.session() as session:
            wallets = await self.repo.get_all(
                session
            )
        return wallets
        # return self.repo.get_all()

class GetWallet:
    def __init__(
        self,
        session: AsyncSession,
        repo: WalletRepository,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self, wallet_id: int,
    ) -> Wallet:
        async with self.session() as session:
            wallet = await self.repo.get_by_id(
                session, wallet_id
            )
            if not wallet:
                raise NotFound("wallet", wallet_id)
        return wallet

class CreateWallet:
    def __init__(
        self,
        session: AsyncSession,
        repo: WalletRepository,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(self, name: str) -> Wallet:
        async with self.session.begin() as session:
            wallet = await self.repo.add(session, name=name)

        return wallet

class UpdateWallet:
    def __init__(
        self,
        session: AsyncSession,
        repo: WalletRepository,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self, wallet_id: int, name: str
    ) -> Wallet:
        async with self.session.begin() as session:
            wallet = await self.repo.get_by_id(session, wallet_id)

            if not wallet:
                raise NotFound("wallet", wallet_id)
            wallet.name = name
            await self.repo.update(session, wallet)

        return wallet

class DeleteWallet:
    def __init__(
        self,
        session: AsyncSession,
        repo: WalletRepository,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self, wallet_id: int
    ) -> None:
        async with self.session.begin() as session:
            wallet = await self.repo.get_by_id(session, wallet_id)
            if wallet:
                await self.repo.delete(session, wallet)