from fastapi import Depends
from typing import Annotated
from session.alchemy_session import AlchemySession
from session.abstract_session import AbstractSession

SessionInterface = Annotated[
    AbstractSession, Depends(AlchemySession)
]