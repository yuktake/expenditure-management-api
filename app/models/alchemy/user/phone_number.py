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

from models.pydantic.user import UserPhoneNumber

class UserPhoneNumberORM(BaseORM):
    __tablename__ = "user_phone_numbers"
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id", ondelete="CASCADE"
        ),
        primary_key=True,
    )
    phone_number: Mapped[str] = mapped_column(String(13))
    user: Mapped["UserORM"] = relationship(
        back_populates="user_phone_number"
    )

    @classmethod
    def from_entity(cls, user_phone_number: UserPhoneNumber):
        return cls(
            user_id=user_phone_number.user_id,
            phone_number=user_phone_number.phone_number,
        )

    def to_entity(self) -> UserPhoneNumber:
        return UserPhoneNumber.model_validate(self)