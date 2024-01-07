from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession as ass

from models.pydantic.user import User
from .abstract_user_repository import AbstractUserRepository
from models.alchemy.user.user import UserORM

class TestUserRepository(AbstractUserRepository):

    async def add(self, session: ass, user: User) -> User:
        return User(id=1, created_at=datetime(2021, 12, 24, 3, 30, 20))

    async def get_by_id(self, session: ass, user_id: int) -> User | None:
        return User(
            id=1, 
            created_at=datetime(2021, 12, 24, 3, 30, 20)
        )