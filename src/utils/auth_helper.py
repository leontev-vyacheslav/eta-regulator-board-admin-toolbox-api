from datetime import datetime, timedelta, timezone
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.data_access.database_connect import get_async_session
from src.data_models.user_data_model import UserDataModel

SECRET_KEY = "ee5ebf8abe24338173f9c1ec4c46112199a6b68639a1fb97a61029072b529399"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(request: Request, session: Annotated[AsyncSession, Depends(get_async_session)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
    try:
        token = request.headers.get("Authorization").replace('Bearer ', '')
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = (await session.scalars(select(UserDataModel).where(UserDataModel.login == username))).first()

    if user is None:
        raise credentials_exception
    return user
