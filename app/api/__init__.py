from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Security,
    status,
)
from fastapi.security import APIKeyHeader
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

router = APIRouter(
    dependencies=[Depends(get_api_key)]
)

router.include_router(admin_router)
router.include_router(auth_router)
router.include_router(wallets_router)