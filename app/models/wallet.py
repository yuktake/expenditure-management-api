from datetime import datetime
from enum import StrEnum
from typing import Annotated
from pydantic import ConfigDict, PositiveInt, Field, validator
from pydantic import WrapSerializer
from utils.datetime import to_utc
from typing import Any
from dataclasses import dataclass

from models.base import BaseModel
from models.history import History

@dataclass(frozen=True)
class Wallet(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    wallet_id: int|None
    name: str = Field(..., min_length=4, max_length=10)
    histories: list[History]

    @property
    def balance(self) -> int:
        return sum(
            h.amount
            if h.type == HistoryType.INCOME
            else -h.amount
            for h in self.histories
        )

    # 独自関数でのValidationも可能
    # @validator("name", pre=True)
    # def test(cls, v: Any) -> Any:
    #     raise NotImplementedError()