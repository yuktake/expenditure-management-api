from fastapi import APIRouter, Depends, status
from typing import Annotated

from .schemas import LoginRequest, LoginResponse
from .use_case import Login
from routes import LoggingRoute

router = APIRouter(
    prefix="/v1", route_class=LoggingRoute
)

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK
)
async def post_login(
    data: LoginRequest,
    use_case: Annotated[Login, Depends(Login)],
) -> LoginResponse:

    return LoginResponse.model_validate(
        await use_case.execute(email=data.email, password=data.password)
    )