from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from models.pydantic.user import User

class AbstractUserRepository(ABC):

    @abstractmethod
    async def add(self, session: AsyncSession, name: str) -> User:
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self,session: AsyncSession, user_id: int,) -> User | None:
        raise NotImplementedError()