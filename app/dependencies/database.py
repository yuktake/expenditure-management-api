from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker
from database import get_session

AsyncSession = Annotated[
    async_sessionmaker, Depends(get_session)
]