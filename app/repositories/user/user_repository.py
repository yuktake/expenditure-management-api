from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession as ass

from models.pydantic.user.user import User
from api.admin.users.schemas import CreateUserRequest
from .abstract_user_repository import AbstractUserRepository
from models.alchemy.user.user import UserORM
from models.alchemy.user.detail import UserDetailORM
from models.alchemy.user.email import UserEmailORM
from models.alchemy.user.password import UserPasswordORM
from models.alchemy.user.phone_number import UserPhoneNumberORM
from models.alchemy.user.active import UserActiveORM

class UserRepository(AbstractUserRepository):

    async def add(self, session: ass, data: CreateUserRequest) -> User:
        user_orm = UserORM(
            cognito_token=None,
            created_at=datetime.now(),
        )
        session.add(user_orm)
        await session.flush()

        user_detail_orm = UserDetailORM(
            user_id=user_orm.id,
            first_name=data.first_name,
            last_name=data.last_name,
        )
        session.add(user_detail_orm)

        user_email_orm = UserEmailORM(
            user_id=user_orm.id,
            email=data.email,
        )
        session.add(user_email_orm)

        user_password_orm = UserPasswordORM(
            user_id=user_orm.id,
            password=data.password,
        )
        session.add(user_password_orm)

        user_phone_number_orm = UserPhoneNumberORM(
            user_id=user_orm.id,
            phone_number=data.phone_number,
        )
        session.add(user_phone_number_orm)

        # TODO:: /UserCognitoToken

        user_active_orm = UserActiveORM(
            user_id=user_orm.id,
            created_at=datetime.now(),
        )
        session.add(user_active_orm)

        await session.flush()

        return user_orm.to_entity()

    async def get_by_id(self, session: ass, user_id: int,) -> User | None:
        stmt = (
            select(UserORM)
            .where(UserORM.id == user_id)
            .options(
                joinedload(UserORM.detail),
                joinedload(UserORM.email),
                joinedload(UserORM.password),
                joinedload(UserORM.cognito_token),
                joinedload(UserORM.phone_number),
            )
        )
        user = await session.scalar(stmt)
        if not user:
            return None

        return user.to_entity()