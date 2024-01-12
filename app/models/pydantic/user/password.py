from dataclasses import dataclass

from pydantic import Field

from models.pydantic.base import BaseModel

@dataclass(frozen=True)
class UserPassword(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    user_id: int
    password: str = Field(..., min_length=8)