from models.alchemy.base import BaseORM
from sqlalchemy import (
    ForeignKey,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from models.pydantic.user import UserPassword

class UserPasswordORM(BaseORM):
    __tablename__ = "user_passwords"
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id", ondelete="CASCADE"
        ),
        primary_key=True,
    )
    password: Mapped[str] = mapped_column(String(255))
    user: Mapped["UserORM"] = relationship(
        back_populates="user_password"
    )

    @classmethod
    def from_entity(cls, user_password: UserPassword):
        return cls(
            user_id=user_password.user_id,
            password=user_password.password,
        )

    def to_entity(self) -> UserPassword:
        return UserPassword.model_validate(self)