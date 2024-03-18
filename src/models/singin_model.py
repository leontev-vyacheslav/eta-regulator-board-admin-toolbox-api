from pydantic import BaseModel


class SingInModel(BaseModel):
    login: str

    password: str

    class Config:
        from_attributes = True
