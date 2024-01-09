import hmac
import hashlib
import base64

import boto3

from config import Settings
from dependencies.repository import UserRepositoryInterface
from dependencies.session import SessionInterface
from .schemas import (
    AdminInitiateAuthResponse,
    SetPasswordResponse,
    LoginResponse
)

class Login:
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

class SetPassword:
    async def execute(
        self,
        email: str,
        new_password: str,
        session: str,
    ) -> SetPasswordResponse:
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

        return SetPasswordResponse(
            challege_type=response['ChallengeName'],
            session=response['Session']
        )

class VerifySmsCode:
    async def execute(
        self,
        email: str,
        code: str,
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
            ChallengeName='SMS_MFA',
            ChallengeResponses={'USERNAME': email, 'SMS_MFA_CODE': code},
            Session=session
        )

        return LoginResponse(
            token=response['AuthenticationResult']['AccessToken']
        )