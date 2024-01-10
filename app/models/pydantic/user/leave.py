from dataclasses import dataclass

from pydantic import Field

from models.pydantic.base import BaseModel
from dependencies.datetime import UTCDatetime

@dataclass(frozen=True)
class UserLeave(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    user_id: int|None
    created_at: UTCDatetime