from abc import ABC, abstractmethod

from api.auth.schemas import (
    AdminInitiateAuthResponse,
    LoginResponse,
    ChangePasswordResponse,
    LogoutResponse,
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
    
class AbstractChangePassword(ABC):

    @abstractmethod
    async def execute(
        self,
        previous_password: str,
        proposed_password: str,
        access_token: str,
    ) -> ChangePasswordResponse:
        raise NotImplementedError()
    
class AbstractLogout(ABC):

    @abstractmethod
    async def execute(self) -> LogoutResponse:
        raise NotImplementedError()