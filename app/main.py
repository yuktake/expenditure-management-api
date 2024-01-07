from contextlib import asynccontextmanager
from database import create_database_if_not_exist
from fastapi import FastAPI, Header, Path, Query
from api import router as api_router
from exceptions import init_exception_handler
from log import init_log
from middlewares import init_middlewares
from config import Settings

# NOTE:: create_database_if_not_exist前にORMクラスを事前にimportしておく必要がある
# またはDIで間接的にimportされている場合もある
from models.alchemy.user.user import UserORM
from models.alchemy.user.detail import UserDetailORM
from models.alchemy.user.email import UserEmailORM
from models.alchemy.user.password import UserPasswordORM
from models.alchemy.user.cognito_token import UserCognitoTokenORM
from models.alchemy.user.phone_number import UserPhoneNumberORM
from models.alchemy.user.active import UserActiveORM
from models.alchemy.user.leave import UserLeaveORM

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 最初のリクエストの処理前に行われる前処理を記述
    print("startup")
    await create_database_if_not_exist()
    yield
    # 最後のリクエストの処理後に行われる後処理を記述
    print("shutdown")

app = FastAPI(titie="MyWallets API", lifespan=lifespan)
init_log()
init_exception_handler(app)
init_middlewares(app)
app.include_router(api_router, prefix="/api")