from models.pydantic.base import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    user_id: int
    token: str

class SmsRequest(BaseModel):
    verification_code: str