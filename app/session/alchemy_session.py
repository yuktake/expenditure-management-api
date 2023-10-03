from .abstract_session import AbstractSession
from dependencies.database import AsyncSession

class AlchemySession(AbstractSession):
    def __init__(self, session: AsyncSession,) -> None:
        self.session = session

    def get_session(self) -> AsyncSession:
        return self.session
