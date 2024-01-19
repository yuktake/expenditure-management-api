import boto3

from config import Settings
from api.auth.schemas import (
    AdminInitiateAuthResponse,
    LoginResponse
)
from .abstract_auth_usecase import(
    AbstractLogin,
    AbstractSetPassword,
)

class Login(AbstractLogin):
    async def execute(
        self,
        email: str,
        password: str
    ) -> AdminInitiateAuthResponse:
        settings = Settings()

        cognito = boto3.client(
            'cognito-idp',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )
        
        response = cognito.admin_initiate_auth(
            UserPoolId=settings.pool_id, 
            ClientId=settings.app_client_id,
            AuthFlow='ADMIN_USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password,
            }
        )

        return AdminInitiateAuthResponse(
            challege_type=response['ChallengeName'],
            session=response['Session']
        )

class SetPassword(AbstractSetPassword):
    async def execute(
        self,
        email: str,
        new_password: str,
        session: str,
    ) -> LoginResponse:
        settings = Settings()

        cognito = boto3.client(
            'cognito-idp',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )

        response = cognito.admin_respond_to_auth_challenge(
            UserPoolId=settings.pool_id,
            ClientId=settings.app_client_id,
            ChallengeName='NEW_PASSWORD_REQUIRED',
            ChallengeResponses={'USERNAME': email, 'NEW_PASSWORD': new_password},
            Session=session
        )

        return LoginResponse(
            access_token=response['AuthenticationResult']['AccessToken'],
            refresh_token=response['AuthenticationResult']['RefreshToken'],
            expires_in=response['AuthenticationResult']['ExpiresIn'],
        )