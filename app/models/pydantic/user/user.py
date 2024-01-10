from dataclasses import dataclass
from typing import Optional

from pydantic import Field

from dependencies.datetime import UTCDatetime
from models.pydantic.base import BaseModel
from models.pydantic.user.detail import UserDetail
from models.pydantic.user.email import UserEmail
from models.pydantic.user.password import UserPassword
from models.pydantic.user.phone_number import UserPhoneNumber
from models.pydantic.user.cognito_token import UserCognitoToken

@dataclass(frozen=True)
class User(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    id: int|None
    detail: UserDetail
    email: Optional[UserEmail]
    password: Optional[UserPassword]
    phone_number: Optional[UserPhoneNumber]
    cognito_token: Optional[UserCognitoToken]
    created_at: UTCDatetime