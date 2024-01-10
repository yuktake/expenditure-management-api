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

from usecases.wallet.history.abstract_history_usecase import (
    AbstractListHistories,
    AbstractGetHistory,
    AbstractCreateHistory,
    AbstractUpdateHistory,
    AbstractDeleteHistory,
    AbstractMoveHistory,
)
from usecases.wallet.history.test_history_usecase import (
    ListHistories as TestListHistories,
    GetHistory as TestGetHistory,
    CreateHistory as TestCreateHistory,
    UpdateHistory as TestUpdateHistory,
    DeleteHistory as TestDeleteHistory,
    MoveHistory as TestMoveHistory,
)
from usecases.wallet.history.history_usecase import (
    ListHistories,
    GetHistory,
    CreateHistory,
    UpdateHistory,
    DeleteHistory,
    MoveHistory,
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

    ListHistoriesInterface = Annotated[
        AbstractListHistories, Depends(TestListHistories)
    ]
    GetHistoryInterface = Annotated[
        AbstractGetHistory, Depends(TestGetHistory)
    ]
    CreateHistoryInterface = Annotated[
        AbstractCreateHistory, Depends(TestCreateHistory)
    ]
    UpdateHistoryInterface = Annotated[
        AbstractUpdateHistory, Depends(TestUpdateHistory)
    ]
    DeleteHistoryInterface = Annotated[
        AbstractDeleteHistory, Depends(TestDeleteHistory)
    ]
    MoveHistoryInterface = Annotated[
        AbstractMoveHistory, Depends(TestMoveHistory)
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

    ListHistoriesInterface = Annotated[
        AbstractListHistories, Depends(ListHistories)
    ]
    GetHistoryInterface = Annotated[
        AbstractGetHistory, Depends(GetHistory)
    ]
    CreateHistoryInterface = Annotated[
        AbstractCreateHistory, Depends(CreateHistory)
    ]
    UpdateHistoryInterface = Annotated[
        AbstractUpdateHistory, Depends(UpdateHistory)
    ]
    DeleteHistoryInterface = Annotated[
        AbstractDeleteHistory, Depends(DeleteHistory)
    ]
    MoveHistoryInterface = Annotated[
        AbstractMoveHistory, Depends(MoveHistory)
    ]