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

from models.pydantic.user import (
    User,
    UserDetail,
    UserEmail,
    UserPassword,
    UserCognitoToken,
    UserPhoneNumber,
    UserActive,
    UserLeave,
)

class UserDetailORM(BaseORM):
    __tablename__ = "user_details"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id", ondelete="CASCADE"
        ),
        index=True,
        unique=True,
    )
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    user: Mapped["UserORM"] = relationship(
        back_populates="user_detail"
    )

    @classmethod
    def from_entity(cls, user_detail: UserDetail):
        return cls(
            id=user_detail.id,
            user_id=user_detail.user_id,
            first_name=user_detail.first_name,
            last_name=user_detail.last_name,
        )

    def to_entity(self) -> UserDetail:
        return UserDetail.model_validate(self)

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

    @classmethod
    def from_entity(cls, user: User):
        return cls(
            user_id=user.user_id,
            created_at=user.created_at
        )

    def to_entity(self) -> User:
        return User.model_validate(self)