from enum import StrEnum
from pydantic import PositiveInt
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
    type: HistoryType
    history_at: UTCDatetime
    wallet_id: int