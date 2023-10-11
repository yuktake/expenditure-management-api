from fastapi import Depends
from typing import Annotated

from repositories.abstract_wallet_repository import AbstractWalletRepository
from repositories.wallet_repository import WalletRepository
from repositories.test_wallet_repository import TestWalletRepository
from config import Settings

settings = Settings()

if settings.status == "testing":
    WalletRepositoryInterface = Annotated[
        AbstractWalletRepository, Depends(TestWalletRepository)
    ]
else:
    WalletRepositoryInterface = Annotated[
        AbstractWalletRepository, Depends(WalletRepository)
    ]