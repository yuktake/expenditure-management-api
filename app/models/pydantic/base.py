from datetime import datetime
from enum import StrEnum
from typing import Annotated
from pydantic import ConfigDict, PositiveInt, Field, validator, WrapSerializer, BaseModel as _BaseModel
from utils.datetime import to_utc
from typing import Any
from dataclasses import dataclass

class BaseModel(_BaseModel):
    # 変数名を揃えることでORMインスタンスからPydanticインスタンスに変換できる？
    model_config = ConfigDict(from_attributes=True)