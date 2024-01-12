from dataclasses import dataclass

from models.pydantic.base import BaseModel
from dependencies.datetime import UTCDatetime

@dataclass(frozen=True)
class UserCognitoToken(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    user_id: int
    # おそらくrefresh_tokenでaccess_tokenはSESSION/SESSION_IDはCookieに持たせる？
    token: str
    created_at: UTCDatetime
    expired_at: UTCDatetime