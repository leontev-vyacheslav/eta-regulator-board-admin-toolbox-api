from pydantic import BaseModel


class AccessTokenModel(BaseModel):
    token: str
