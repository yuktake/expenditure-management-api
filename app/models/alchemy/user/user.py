from models.alchemy.base import BaseORM
from datetime import datetime
from sqlalchemy import (
    ForeignKey,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from models.pydantic.user import User
from models.alchemy.user.detail import UserDetailORM
from models.alchemy.user.email import UserEmailORM
from models.alchemy.user.password import UserPasswordORM
from models.alchemy.user.cognito_token import UserCognitoTokenORM
from models.alchemy.user.phone_number import UserPhoneNumberORM

class UserORM(BaseORM):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime]
    user_detail: Mapped[UserDetailORM] = relationship(
        back_populates="user",
        cascade=(
            "save-update, merge, expunge"
            ", delete, delete-orphan"
        ),
    )
    user_email: Mapped[UserEmailORM] = relationship(
        back_populates="user",
        cascade=(
            "save-update, merge, expunge"
            ", delete, delete-orphan"
        ),
    )
    user_cognito_token: Mapped[UserCognitoTokenORM] = relationship(
        back_populates="user",
        cascade=(
            "save-update, merge, expunge"
            ", delete, delete-orphan"
        ),
    )
    user_phone_number: Mapped[UserPhoneNumberORM] = relationship(
        back_populates="user",
        cascade=(
            "save-update, merge, expunge"
            ", delete, delete-orphan"
        ),
    )

    @classmethod
    def from_entity(cls, user: User):
        return cls(
            user_id=user.user_id,
            created_at=user.created_at
        )

    def to_entity(self) -> User:
        return User.model_validate(self)