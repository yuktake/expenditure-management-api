from dataclasses import dataclass

from pydantic import Field

from dependencies.datetime import UTCDatetime
from models.pydantic.base import BaseModel

@dataclass(frozen=True)
class User(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    id: int|None
    created_at: UTCDatetime