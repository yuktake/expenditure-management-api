from models.alchemy.base import BaseORM
from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from models.pydantic.user import UserDetail

class UserDetailORM(BaseORM):
    __tablename__ = "user_details"
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "users.id", ondelete="CASCADE"
        ),
        primary_key=True,
    )
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    user: Mapped["UserORM"] = relationship(
        back_populates="detail"
    )

    @classmethod
    def from_entity(cls, user_detail: UserDetail):
        return cls(
            user_id=user_detail.user_id,
            first_name=user_detail.first_name,
            last_name=user_detail.last_name,
        )

    def to_entity(self) -> UserDetail:
        return UserDetail.model_validate(self)