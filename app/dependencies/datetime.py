from typing import Annotated
from datetime import datetime
from pydantic import WrapSerializer
from utils.datetime import to_utc

UTCDatetime = Annotated[datetime, WrapSerializer(to_utc)]