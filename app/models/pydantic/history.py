from enum import StrEnum
from pydantic import PositiveInt, Field
from dataclasses import dataclass

from dependencies.datetime import UTCDatetime
from models.pydantic.base import BaseModel

class HistoryType(StrEnum):
    INCOME = "INCOME"
    OUTCOME = "OUTCOME"

@dataclass(frozen=True)
class History(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    history_id: int|None
    name: str
    amount: PositiveInt
    type: HistoryType = Field(..., description="INCOME:収入, OUTCOME:支出")
    history_at: UTCDatetime = Field(..., description="収支項目の発生日時（UTC）")
    wallet_id: int