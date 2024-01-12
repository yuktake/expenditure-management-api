from models.alchemy.base import BaseORM
from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from .history import HistoryORM
from models.pydantic.history import History, HistoryType
from models.pydantic.wallet import Wallet

class WalletORM(BaseORM):
    __tablename__ = "wallets"
    wallet_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    histories: Mapped[
        list[HistoryORM]
    ] = relationship(
        back_populates="wallet",
        order_by=HistoryORM.history_at.desc(),
        cascade=(
            "save-update, merge, expunge"
            ", delete, delete-orphan"
        ),
    )

    @classmethod
    def from_entity(cls, wallet: Wallet):
        return cls(
            wallet_id=wallet.wallet_id,
            name=wallet.name,
            histories=wallet.histories,
        )

    def to_entity(self) -> Wallet:
        return Wallet.model_validate(self)

    def update(self, wallet: Wallet, histories: list[HistoryORM]) -> None:
        self.name = wallet.name
        self.histories = histories