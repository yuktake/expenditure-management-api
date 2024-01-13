from typing import Annotated
from datetime import datetime

from pydantic import WrapSerializer

from utils.datetime import to_utc
from config import Settings

settings = Settings()

if settings.status == "testing":
    # テスト用の特定の日時を返すdatetimeを定義することで、現在時刻等の変動する値を固定できる
    UTCDatetime = Annotated[datetime, WrapSerializer(to_utc)]
else:
    UTCDatetime = Annotated[datetime, WrapSerializer(to_utc)]