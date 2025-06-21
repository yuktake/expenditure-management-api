import boto3

from config import Settings
from api.auth.schemas import (
    AdminInitiateAuthResponse,
    LoginResponse,
    ChangePasswordResponse,
    LogoutResponse,
    ErrorResponse
)
from .abstract_auth_usecase import(
    AbstractLogin,
    AbstractSetPassword,
    AbstractChangePassword,
    AbstractLogout,
)

settings = Settings()

cognito = boto3.client(
    'cognito-idp',
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region,
)

class Login(AbstractLogin):
    async def execute(
        self,
        email: str,
        password: str
    ) -> AdminInitiateAuthResponse:
        print("testing")
        
        try:
            response = cognito.admin_initiate_auth(
                UserPoolId=settings.pool_id, 
                ClientId=settings.app_client_id,
                AuthFlow='ADMIN_USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password,
                }
            )
        except Exception as e:
            return ErrorResponse(message=str(e))

        if 'Session' not in response:
            return LoginResponse(
                access_token=response['AuthenticationResult']['AccessToken'],
                refresh_token=response['AuthenticationResult']['RefreshToken'],
                expires_in=response['AuthenticationResult']['ExpiresIn'],
            )


        return AdminInitiateAuthResponse(
            challege_type=response['ChallengeName'],
            session=response['Session'],
        )

class SetPassword(AbstractSetPassword):
    async def execute(
        self,
        email: str,
        new_password: str,
        session: str,
    ) -> LoginResponse:
        print("testing")

        try:
            response = cognito.admin_respond_to_auth_challenge(
                UserPoolId=settings.pool_id,
                ClientId=settings.app_client_id,
                ChallengeName='NEW_PASSWORD_REQUIRED',
                ChallengeResponses={'USERNAME': email, 'NEW_PASSWORD': new_password},
                Session=session
            )
        except Exception as e:
            return ErrorResponse(message=str(e))

        return LoginResponse(
            access_token=response['AuthenticationResult']['AccessToken'],
            refresh_token=response['AuthenticationResult']['RefreshToken'],
            expires_in=response['AuthenticationResult']['ExpiresIn'],
        )
    
class ChangePassword(AbstractChangePassword):
    async def execute(
        self,
        previous_password: str,
        proposed_password: str,
        access_token: str,
    ) -> ChangePasswordResponse:
        print("testing")

        try:
            cognito.change_password(
                PreviousPassword=previous_password,
                ProposedPassword=proposed_password,
                AccessToken=access_token
            )
        except Exception as e:
            return ErrorResponse(message=str(e))
        
        return ChangePasswordResponse(
            result=True,
        )
    
class Logout(AbstractLogout):
    async def execute(self) -> LogoutResponse:
        try:
            cognito.admin_user_global_sign_out(
                UserPoolId=settings.pool_id,
                Username="7f5b4afa-2dd5-4896-a44c-5e6845403039",
            )
        except Exception as e:
            return ErrorResponse(message=str(e))
        
        return LogoutResponse(
            result=True,
        )