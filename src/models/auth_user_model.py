from pydantic import BaseModel


class AuthUserModel (BaseModel):
    token: str
    
    login: str

    class Config:
        from_attributes = True
