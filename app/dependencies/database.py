from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker
from database import get_session
from config import Settings

settings = Settings()

if settings.status == "testing":
    AsyncSession = Annotated[
        async_sessionmaker, Depends(get_session)
    ]
else:
    AsyncSession = Annotated[
        async_sessionmaker, Depends(get_session)
    ]

