from dataclasses import dataclass

from pydantic import Field

from models.pydantic.base import BaseModel

@dataclass(frozen=True)
class UserDetail(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    user_id: int
    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)