from fastapi import Depends
from typing import Annotated

from repositories.wallet.abstract_wallet_repository import AbstractWalletRepository
from repositories.wallet.wallet_repository import WalletRepository
from repositories.wallet.test_wallet_repository import TestWalletRepository

from repositories.user.abstract_user_repository import AbstractUserRepository
from repositories.user.user_repository import UserRepository
from repositories.user.test_user_repository import TestUserRepository

from config import Settings

settings = Settings()

if settings.status == "testing":
    WalletRepositoryInterface = Annotated[
        AbstractWalletRepository, Depends(TestWalletRepository)
    ]
    UserRepositoryInterface = Annotated[
        AbstractUserRepository, Depends(TestUserRepository)
    ]
else:
    WalletRepositoryInterface = Annotated[
        AbstractWalletRepository, Depends(WalletRepository)
    ]
    UserRepositoryInterface = Annotated[
        AbstractUserRepository, Depends(UserRepository)
    ]