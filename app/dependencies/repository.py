from fastapi import Depends
from typing import Annotated

from repositories.abstract_wallet_repository import AbstractWalletRepository
from repositories.wallet_repository import WalletRepository

WalletRepositoryInterface = Annotated[
    AbstractWalletRepository, Depends(WalletRepository)
]