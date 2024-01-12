import json
import time

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Security,
    status,
)
from fastapi.security import APIKeyHeader, APIKeyCookie
from .wallets.views import router as wallets_router
from .admin.users.views import router as admin_router
from .auth.views import router as auth_router

async def get_api_key(
    api_key_header: str = Security(
        APIKeyHeader(
            name="APP-API-KEY",
            auto_error=True
        )
    ),
) -> str:
    if api_key_header != "DUMMY-KEY":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN
        )

    return api_key_header

async def get_access_token(
        cookie: str = Security(
            APIKeyCookie(
                name="session",
                # Cookieの値がない場合はエラーにする
                auto_error=True,
            )
        ),
) -> str:
    # TODO: CognitoTokenの検証
    decoded_cookie = json.loads(cookie)
    # トークンの期限が切れている場合はリフレッシュトークンを使ってトークンを更新する
    if decoded_cookie["exp"] < time.time():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    return cookie

router = APIRouter(
    dependencies=[Depends(get_api_key)]
    # dependencies=[Depends(get_access_token)]
)

router.include_router(admin_router)
router.include_router(auth_router)
router.include_router(wallets_router)