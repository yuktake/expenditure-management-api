from pydantic import Field
from dataclasses import dataclass

from dependencies.datetime import UTCDatetime
from models.pydantic.base import BaseModel

@dataclass(frozen=True)
class User(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    id: int|None
    created_at: UTCDatetime

@dataclass(frozen=True)
class UserDetail(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    user_id: int
    first_name: str = Field(..., max_length=255)
    last_name: str = Field(..., max_length=255)

@dataclass(frozen=True)
class UserEmail(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    user_id: int
    email: str

@dataclass(frozen=True)
class UserPassword(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    user_id: int
    password: str = Field(..., min_length=8)

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

@dataclass(frozen=True)
class UserPhoneNumber(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    user_id: int
    phone_number: str = Field(..., min_length=11, max_length=11)

@dataclass(frozen=True)
class UserActive(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    user_id: int|None
    created_at: UTCDatetime

@dataclass(frozen=True)
class UserLeave(BaseModel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model_validate(self)

    user_id: int|None
    created_at: UTCDatetime