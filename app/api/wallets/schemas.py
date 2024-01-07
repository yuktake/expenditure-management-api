from pydantic import Field
from models.pydantic.base import BaseModel
from models.pydantic.wallet import Wallet
from .histories.schemas import History

class GetWalletsResponse(BaseModel):
    wallets: list[Wallet]

class GetWalletResponse(Wallet):
    pass

class GetWalletResponseWithHistories(Wallet):
    histories: list[History] = Field(..., description="関連する収支項目一覧")

class PostWalletRequest(BaseModel):
    name: str

class PostWalletResponse(Wallet):
    pass

class PutWalletRequest(BaseModel):
    name: str

class PutWalletResponse(Wallet):
    pass