from dependencies.repository import UserRepositoryInterface
from dependencies.session import SessionInterface
from .schemas import CreateUserRequest, CreateUserResponse

class CreateUser:
    def __init__(
        self,
        session: SessionInterface,
        repo: UserRepositoryInterface,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self,
        data: CreateUserRequest
    ) -> CreateUserResponse:
        sess = self.session.get_session()

        async with sess.begin() as s:
            user = await self.repo.add(s, data)

        return user