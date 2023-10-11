from fastapi import Depends
from typing import Annotated

from session.alchemy_session import AlchemySession
from session.abstract_session import AbstractSession
from config import Settings

settings = Settings()

if settings.status == "testing":
    SessionInterface = Annotated[
        AbstractSession, Depends(AlchemySession)
    ]
else:
    SessionInterface = Annotated[
        AbstractSession, Depends(AlchemySession)
    ]