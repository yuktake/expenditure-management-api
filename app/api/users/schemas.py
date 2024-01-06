from pydantic import Field
from models.pydantic.base import BaseModel
from dependencies.datetime import UTCDatetime

class User(BaseModel):
    user_id: int
    created_at: UTCDatetime = Field(..., description="登録日時（UTC）")