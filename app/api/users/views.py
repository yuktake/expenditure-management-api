from fastapi import APIRouter, Depends, status
from typing import Annotated

from .schemas import CreateUserRequest, CreateUserResponse
from .use_case import CreateUser
from routes import LoggingRoute

router = APIRouter(
    prefix="/v1/user", route_class=LoggingRoute
)

@router.post(
    "",
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    data: CreateUserRequest,
    use_case: Annotated[CreateUser, Depends(CreateUser)],
) -> CreateUserResponse:
    """Userの作成API"""
    return CreateUserResponse.model_validate(
        await use_case.execute(data=data)
    )