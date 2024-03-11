from pydantic import BaseModel


class AccessTokenModel(BaseModel):
    token: str

    class Config:
        from_attributes = True
