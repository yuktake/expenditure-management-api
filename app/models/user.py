from datetime import datetime
from enum import StrEnum
from typing import Annotated
from pydantic import ConfigDict, PositiveInt, Field, validator
from pydantic import WrapSerializer
from utils.datetime import to_utc
from typing import Any
from dataclasses import dataclass
from dependencies.datetime import UTCDatetime

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
    firstName: str = Field(..., max_length=255)
    lastName: str = Field(..., max_length=255)

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
    phoneNumber: str = Field(..., min_length=11, max_length=11)

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