from abc import ABC, abstractmethod

from api.admin.users.schemas import (
    CreateUserRequest, 
    CreateUserResponse,
)

class AbstractCreateUser(ABC):

    @abstractmethod
    async def execute(
        self,
        data: CreateUserRequest
    ) -> CreateUserResponse:
        raise NotImplementedError()