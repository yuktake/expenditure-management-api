from fastapi import Depends
from typing import Annotated

from usecases.wallet.abstract_wallet_usecase import (
    AbstractListWallets,
    AbstractGetWallet,
    AbstractCreateWallet,
    AbstractUpdateWallet,
    AbstractDeleteWallet
)
from usecases.wallet.test_wallet_usecase import (
    ListWallets as TestListWallets,
    GetWallet as TestGetWallet,
    CreateWallet as TestCreateWallet,
    UpdateWallet as TestUpdateWallet,
    DeleteWallet as TestDeleteWallet
)
from usecases.wallet.wallet_usecase import (
    ListWallets,
    GetWallet,
    CreateWallet,
    UpdateWallet,
    DeleteWallet
)
from config import Settings

settings = Settings()

if settings.status == "testing":
    ListWalletsInterface = Annotated[
        AbstractListWallets, Depends(TestListWallets)
    ]
    GetWalletInterface = Annotated[
        AbstractGetWallet, Depends(TestGetWallet)
    ]
    CreateWalletInterface = Annotated[
        AbstractCreateWallet, Depends(TestCreateWallet)
    ]
    UpdateWalletInterface = Annotated[
        AbstractUpdateWallet, Depends(TestUpdateWallet)
    ]
    DeleteWalletInterface = Annotated[
        AbstractDeleteWallet, Depends(TestDeleteWallet)
    ]

else:
    ListWalletsInterface = Annotated[
        AbstractListWallets, Depends(ListWallets)
    ]
    GetWalletInterface = Annotated[
        AbstractGetWallet, Depends(GetWallet)
    ]
    CreateWalletInterface = Annotated[
        AbstractCreateWallet, Depends(CreateWallet)
    ]
    UpdateWalletInterface = Annotated[
        AbstractUpdateWallet, Depends(UpdateWallet)
    ]
    DeleteWalletInterface = Annotated[
        AbstractDeleteWallet, Depends(DeleteWallet)
    ]
