from pydantic import (
    ConfigDict,
    BaseModel as _BaseModel
)

class BaseModel(_BaseModel):
    # 変数名を揃えることでORMインスタンスからPydanticインスタンスに変換できる？
    model_config = ConfigDict(from_attributes=True)