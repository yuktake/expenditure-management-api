from dependencies.repository import UserRepositoryInterface
from dependencies.session import SessionInterface
from .schemas import LoginResponse

class Login:
    def __init__(
        self,
        session: SessionInterface,
        repo: UserRepositoryInterface,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self,
        email: str,
        password: str
    ) -> LoginResponse:
        sess = self.session.get_session()
        async with sess() as s:
            user = await self.repo.get_by_id(s, 1)

        return LoginResponse(
            user_id=user.id,
            token="aaa",
        )