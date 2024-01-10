from typing import Annotated

from fastapi import APIRouter, Depends, status

from .schemas import (
    LoginRequest, 
    AdminInitiateAuthResponse,
    SetPasswordRequest,
    SetPasswordResponse,
    SmsRequest,
    LoginResponse,
)
from dependencies.usecase import(
    LoginInterface,
    SetPasswordInterface,
    VerifySmsCodeInterface,
)
from routes import LoggingRoute

router = APIRouter(
    prefix="/v1", route_class=LoggingRoute
)

@router.post(
    "/login",
    response_model=AdminInitiateAuthResponse,
    status_code=status.HTTP_200_OK
)
async def post_login(
    data: LoginRequest,
    use_case: LoginInterface,
) -> AdminInitiateAuthResponse:

    return AdminInitiateAuthResponse.model_validate(
        await use_case.execute(email=data.email, password=data.password)
    )

@router.post(
    "/set_password",
    response_model=SetPasswordResponse,
    status_code=status.HTTP_200_OK
)
async def post_set_password(
    data: SetPasswordRequest,
    use_case: SetPasswordInterface,
) -> SetPasswordResponse:

    return SetPasswordResponse.model_validate(
        await use_case.execute(
            email=data.email, 
            new_password=data.new_password, 
            session=data.session
        )
    )

@router.post(
    "/verify_sms",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK
)
async def post_verify_sms(
    data: SmsRequest,
    use_case: VerifySmsCodeInterface,
) -> LoginResponse:

    return LoginResponse.model_validate(
        await use_case.execute(
            email=data.email, 
            code=data.code, 
            session=data.session
        )
    )