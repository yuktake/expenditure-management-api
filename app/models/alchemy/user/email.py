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

from models.pydantic.user.email import UserEmail

class UserEmailORM(BaseORM):
    __tablename__ = "user_emails"
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id", 
            ondelete="CASCADE",
        ),
        primary_key=True,
    )
    email: Mapped[str] = mapped_column(String(50))
    user: Mapped["UserORM"] = relationship(
        back_populates="email",
        lazy="joined",
    )

    @classmethod
    def from_entity(cls, user_email: UserEmail):
        return cls(
            user_id=user_email.user_id,
            email=user_email.email,
        )

    def to_entity(self) -> UserEmail:
        return UserEmail.model_validate(self)