import boto3

from config import Settings
from dependencies.repository import UserRepositoryInterface
from dependencies.session import SessionInterface
from api.admin.users.schemas import CreateUserRequest, CreateUserResponse
from .abstract_user_usecase import AbstractCreateUser

class CreateUser(AbstractCreateUser):
    def __init__(
        self,
        session: SessionInterface,
        repo: UserRepositoryInterface,
    ) -> None:
        self.session = session
        self.repo = repo

    async def execute(
        self,
        data: CreateUserRequest
    ) -> CreateUserResponse:
        settings = Settings()
        cognito = boto3.client(
            'cognito-idp',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region,
        )
        cognito_user = cognito.admin_create_user(
            UserPoolId=settings.pool_id, 
            Username=data.email,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': data.email,
                },
                {
                    'Name': 'email_verified',
                    'Value': 'True',
                },
                {
                    'Name': 'phone_number',
                    'Value': data.phone_number,
                },
                {
                    'Name': 'phone_number_verified',
                    'Value': 'True',
                },
            ],
            TemporaryPassword=data.password,
            DesiredDeliveryMediums=[
                'EMAIL',
            ],
            MessageAction='SUPPRESS',
        )

        sess = self.session.get_session()
        async with sess.begin() as s:
            user = await self.repo.add(s, data)

        return user