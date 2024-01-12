from fastapi import APIRouter, status

from .schemas import CreateUserRequest, CreateUserResponse
from dependencies.usecase import (
    CreateUserInterface,
)
from routes import LoggingRoute

router = APIRouter(
    prefix="/v1/admin/users", route_class=LoggingRoute
)

@router.post(
    "",
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    data: CreateUserRequest,
    use_case: CreateUserInterface,
) -> CreateUserResponse:
    """Userの作成API"""
    return CreateUserResponse.model_validate(
        await use_case.execute(data=data)
    )