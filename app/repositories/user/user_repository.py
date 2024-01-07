from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession as ass

from models.pydantic.user import User
from .abstract_user_repository import AbstractUserRepository
from models.alchemy.user.user import UserORM

class UserRepository(AbstractUserRepository):

    async def add(self, session: ass, user: User) -> User:
        user_orm = UserORM(name=wallet.name, histories=[])
        session.add(user_orm)
        await session.flush()
        return user_orm.to_entity()

    async def get_by_id(self, session: ass, user_id: int,) -> User | None:
        stmt = (
            select(UserORM)
            .where(UserORM.id == user_id)
        )
        user = await session.scalar(stmt)
        if not user:
            return None
        return user.to_entity()