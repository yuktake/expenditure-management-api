from contextlib import asynccontextmanager
from db.database import create_database_if_not_exist
from fastapi import FastAPI, Header, Path, Query
from api import router as api_router
from exceptions import init_exception_handler
from log import init_log
from middlewares import init_middlewares
# from containers import Container
from config import Settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 最初のリクエストの処理前に行われる前処理を記述
    print("startup")
    await create_database_if_not_exist()
    yield
    # 最後のリクエストの処理後に行われる後処理を記述
    print("shutdown")

# container = Container()

app = FastAPI(titie="MyWallets API", lifespan=lifespan)

# app.container = container
init_log()
init_exception_handler(app)
init_middlewares(app)
app.include_router(api_router, prefix="/api")