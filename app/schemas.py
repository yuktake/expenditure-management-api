from enum import StrEnum
from typing import Annotated
from pydantic import BaseModel, Field, PositiveInt, SerializerFunctionWrapHandler, WrapSerializer
from datetime import datetime, timezone

class HistoryType(StrEnum):
    INCOME = "INCOME"
    OUTCOME = "OUTCOME"

class History(BaseModel):
    history_id: int
    name: str
    amount: PositiveInt
    type: HistoryType
    history_at: datetime

class CreateWalletRequest(BaseModel):
    name: str