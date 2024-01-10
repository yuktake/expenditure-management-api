from dataclasses import dataclass

from pydantic import Field

from models.pydantic.base import BaseModel

@dataclass(frozen=True)
class UserPhoneNumber(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    user_id: int
    phone_number: str = Field(..., min_length=11, max_length=11)