from dataclasses import dataclass

from models.pydantic.base import BaseModel

@dataclass(frozen=True)
class UserEmail(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    user_id: int
    email: str