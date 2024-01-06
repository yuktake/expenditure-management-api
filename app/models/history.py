from datetime import datetime
from enum import StrEnum
from typing import Annotated
from pydantic import ConfigDict, PositiveInt, Field, validator
from pydantic import WrapSerializer
from utils.datetime import to_utc
from typing import Any
from dataclasses import dataclass

from dependencies.datetime import UTCDatetime
from models.base import BaseModel

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