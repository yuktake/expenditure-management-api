from datetime import datetime

from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from models.alchemy.base import BaseORM
from models.pydantic.user.active import UserActive

class UserActiveORM(BaseORM):
    __tablename__ = "user_actives"
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id", ondelete="CASCADE"
        ),
        primary_key=True,
    )
    created_at: Mapped[datetime]

    @classmethod
    def from_entity(cls, user_active: UserActive):
        return cls(
            user_id=user_active.user_id,
            created_at=user_active.created_at,
        )

    def to_entity(self) -> UserActive:
        return UserActive.model_validate(self)