from abc import ABC, abstractmethod

from api.auth.schemas import (
    AdminInitiateAuthResponse,
    LoginResponse,
)

class AbstractLogin(ABC):

    @abstractmethod
    async def execute(
        self,
        email: str,
        password: str
    ) -> AdminInitiateAuthResponse:
        raise NotImplementedError()

class AbstractSetPassword(ABC):

    @abstractmethod
    async def execute(
        self,
        email: str,
        new_password: str,
        session: str,
    ) -> LoginResponse:
        raise NotImplementedError()