from pydantic import Field, field_validator
from dataclasses import dataclass

from models.pydantic.base import BaseModel
from models.pydantic.history import History, HistoryType

@dataclass(frozen=True)
class Wallet(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    wallet_id: int|None
    name: str = Field(..., max_length=10)
    histories: list[History]

    # 現在時点の予算
    @property
    def balance(self) -> int:
        return sum(
            h.amount
            if h.type == HistoryType.INCOME
            else -h.amount
            for h in self.histories
        )

    # 独自関数でのValidationも可能
    @field_validator("name", mode="before")
    def name_validation(cls, v: str) -> str:
        if v == "test":
            raise ValueError("test is not allowed")
        
        return v