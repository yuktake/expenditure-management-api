from datetime import datetime
from sqlalchemy import (
    CheckConstraint,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)
from models.pydantic.history import History, HistoryType
from models.pydantic.wallet import Wallet


class BaseORM(DeclarativeBase):
    pass

class HistoryORM(BaseORM):
    __tablename__ = "histories"
    history_id: Mapped[int] = mapped_column(
        primary_key=True
    )
    name: Mapped[str] = mapped_column(String(50))
    amount: Mapped[int] = mapped_column(
        Integer, CheckConstraint("amount > 0")
    )
    type: Mapped[HistoryType] = mapped_column(
        Enum(HistoryType)
    )
    wallet_id: Mapped[int] = mapped_column(
        ForeignKey(
            "wallets.wallet_id", ondelete="CASCADE"
        ),
        index=True,
    )
    history_at: Mapped[datetime]
    wallet: Mapped["WalletORM"] = relationship(
        back_populates="histories"
    )

    @classmethod
    def from_entity(cls, history: History):
        return cls(
            history_id=history.history_id,
            name=history.name,
            amount=history.amount,
            type=history.type,
            wallet_id=history.wallet_id,
            history_at=history.history_at,
        )

    def to_entity(self) -> History:
        return History.model_validate(self)

    def update(self, history: History) -> None:
        self.name = history.name
        self.amount = history.amount
        self.type = history.type
        self.wallet_id = history.wallet_id
        self.history_at = history.history_at

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