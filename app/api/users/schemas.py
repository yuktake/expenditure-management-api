from pydantic import Field
from models.pydantic.base import BaseModel
from dependencies.datetime import UTCDatetime

from models.pydantic.base import BaseModel
from models.pydantic.user import User

class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: str

class CreateUserResponse(User):
    pass