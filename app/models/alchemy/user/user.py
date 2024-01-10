from datetime import datetime
from typing import Optional

from sqlalchemy import (
    ForeignKey,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from models.alchemy.base import BaseORM
from models.pydantic.user.user import User

class UserORM(BaseORM):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime]
    detail: Mapped["UserDetailORM"] = relationship(
        back_populates="user",
        cascade=(
            "save-update, merge, expunge"
            ", delete, delete-orphan"
        ),
        lazy="joined"
    )
    email: Mapped[Optional["UserEmailORM"]] = relationship(
        back_populates="user",
        cascade=(
            "save-update, merge, expunge"
            ", delete, delete-orphan"
        ),
        lazy="joined"
    )
    password: Mapped[Optional["UserPasswordORM"]] = relationship(
        back_populates="user",
        cascade=(
            "save-update, merge, expunge"
            ", delete, delete-orphan"
        ),
        lazy="joined"
    )
    cognito_token: Mapped[Optional["UserCognitoTokenORM"]] = relationship(
        back_populates="user",
        cascade=(
            "save-update, merge, expunge"
            ", delete, delete-orphan"
        ),
        lazy="joined",
    )
    phone_number: Mapped[Optional["UserPhoneNumberORM"]] = relationship(
        back_populates="user",
        cascade=(
            "save-update, merge, expunge"
            ", delete, delete-orphan"
        ),
        lazy="joined"
    )

    @classmethod
    def from_entity(cls, user: User):
        return cls(
            user_id=user.user_id,
            created_at=user.created_at
        )

    def to_entity(self) -> User:
        return User.model_validate(self)