from fastapi import APIRouter, status, Response

from .schemas import (
    LoginRequest, 
    AdminInitiateAuthResponse,
    SetPasswordRequest,
    LoginResponse,
    ChangePasswordRequest,
    ChangePasswordResponse,
    LogoutRequest,
    LogoutResponse,
    ErrorResponse
)
from dependencies.usecase import(
    LoginInterface,
    SetPasswordInterface,
    ChangePasswordInterface,
    LogoutInterface,
)
from routes import LoggingRoute

router = APIRouter(
    prefix="/v1", route_class=LoggingRoute
)

@router.post(
    "/login",
    response_model=AdminInitiateAuthResponse|LoginResponse|ErrorResponse,
    status_code=status.HTTP_200_OK
)
async def post_login(
    data: LoginRequest,
    use_case: LoginInterface,
) -> AdminInitiateAuthResponse|LoginResponse|ErrorResponse:
    
    response = await use_case.execute(email=data.email, password=data.password)
    
    if hasattr(response, 'message'):
        return ErrorResponse.model_validate(
            response
        )
    
    if hasattr(response, 'session'):
        return AdminInitiateAuthResponse.model_validate(
            response
        )
    
    return LoginResponse.model_validate(
        response
    )

@router.post(
    "/set_password",
    response_model=LoginResponse|ErrorResponse,
    status_code=status.HTTP_200_OK
)
async def post_set_password(
    data: SetPasswordRequest,
    use_case: SetPasswordInterface,
) -> LoginResponse|ErrorResponse:
    
    login_response = await use_case.execute(
        email=data.email, 
        new_password=data.new_password, 
        session=data.session
    )

    if hasattr(login_response, 'message'):
        return ErrorResponse.model_validate(
            login_response
        )

    # response.set_cookie(
    #     key="access_token",
    #     value=login_response.token,
    #     httponly=True,
    #     secure=True,
    #     # access_tokenの有効期限より短い時間に設定する
    #     max_age=1800,
    #     # Strice or Laxを指定することで、Cookieが送信される条件を制限できる
    #     Samesite="Strict",
    # )

    return LoginResponse.model_validate(
        login_response
    )

@router.post(
    "/change_password",
    response_model=ChangePasswordResponse|ErrorResponse,
    status_code=status.HTTP_200_OK
)
async def post_change_password(
    data: ChangePasswordRequest,
    use_case: ChangePasswordInterface,
) -> ChangePasswordResponse|ErrorResponse:
    
    response = await use_case.execute(
        previous_password=data.previous_password,
        proposed_password=data.proposed_password,
        access_token=data.access_token,
    )
    
    if hasattr(response, 'message'):
        return ErrorResponse.model_validate(
            response
        )
    
    return ChangePasswordResponse.model_validate(
        response
    )

@router.post(
    "/logout",
    response_model=LogoutResponse|ErrorResponse,
    status_code=status.HTTP_200_OK
)
async def post_logout(
    data: LogoutRequest,
    use_case: LogoutInterface,
) -> LogoutResponse|ErrorResponse:
    #TODO access_tokenからUserを特定したい
    response = await use_case.execute()
    
    if hasattr(response, 'message'):
        return ErrorResponse.model_validate(response)
    
    return LogoutResponse.model_validate(response)