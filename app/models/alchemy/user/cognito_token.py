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

from models.alchemy.base import BaseORM
from models.pydantic.user import UserCognitoToken

class UserCognitoTokenORM(BaseORM):
    __tablename__ = "user_cognito_tokens"
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id", ondelete="CASCADE"
        ),
        primary_key=True,
    )
    token: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime]
    expired_at: Mapped[datetime]
    user: Mapped["UserORM"] = relationship(
        back_populates="user_cognito_token"
    )

    @classmethod
    def from_entity(cls, user_cognito_token: UserCognitoToken):
        return cls(
            user_id=user_cognito_token.user_id,
            token=user_cognito_token.token,
            created_at=user_cognito_token.created_at,
            expired_at=user_cognito_token.expired_at,
        )

    def to_entity(self) -> UserCognitoToken:
        return UserCognitoToken.model_validate(self)