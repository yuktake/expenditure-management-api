from fastapi import APIRouter, status, Response

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
    
    login_response = await use_case.execute(
        email=data.email, 
        code=data.code, 
        session=data.session
    )

    response.set_cookie(
        key="access_token",
        value=login_response.token,
        httponly=True,
        secure=True,
        # access_tokenの有効期限より短い時間に設定する
        max_age=1800,
        # Strice or Laxを指定することで、Cookieが送信される条件を制限できる
        Samesite="Strict",
    )

    return LoginResponse.model_validate(
        login_response
    )