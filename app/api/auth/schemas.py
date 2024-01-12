from enum import StrEnum

from models.pydantic.base import BaseModel

class ChallengeType(StrEnum):
    NEW_PASSWORD_REQUIRED = "NEW_PASSWORD_REQUIRED"
    SMS_MFA = "SMS_MFA"

class LoginRequest(BaseModel):
    email: str
    password: str

class AdminInitiateAuthResponse(BaseModel):
    challege_type: ChallengeType
    session: str

class SetPasswordRequest(BaseModel):
    email: str
    new_password: str
    session: str

class SetPasswordResponse(BaseModel):
    challege_type: ChallengeType
    session: str

class SmsRequest(BaseModel):
    email: str
    code: str
    session: str

class LoginResponse(BaseModel):
    token: str