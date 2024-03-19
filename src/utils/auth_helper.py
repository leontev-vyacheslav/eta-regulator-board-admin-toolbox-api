from functools import wraps
from datetime import datetime, timedelta, timezone
from sqlalchemy import select

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.data_models.user_data_model import UserDataModel
from src.data_access.database_connect import async_session_maker

SECRET_KEY = "ee5ebf8abe24338173f9c1ec4c46112199a6b68639a1fb97a61029072b529399"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


def authorize():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
            request = kwargs.get("request")
            try:
                auth_header = request.headers.get("Authorization")
                if auth_header is not None:
                    token = auth_header.replace('Bearer ', '')
                    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                    username: str = payload.get("sub")
                else:
                    raise credentials_exception

                if username is None:
                    raise credentials_exception
            except JWTError as ex:
                raise credentials_exception from ex

            async with async_session_maker() as session:
                user = (await session.scalars(select(UserDataModel).where(UserDataModel.login == username))).first()

            if user is None:
                raise credentials_exception

            return await func(*args, **kwargs)

        return wrapper

    return decorator
