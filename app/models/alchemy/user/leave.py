from datetime import datetime

from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from models.alchemy.base import BaseORM
from models.pydantic.user.leave import UserLeave

class UserLeaveORM(BaseORM):
    __tablename__ = "user_leaves"
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id", ondelete="CASCADE"
        ),
        primary_key=True,
    )
    created_at: Mapped[datetime]
    
    @classmethod
    def from_entity(cls, user_leave: UserLeave):
        return cls(
            user_id=user_leave.user_id,
            created_at=user_leave.created_at,
        )

    def to_entity(self) -> UserLeave:
        return UserLeave.model_validate(self)