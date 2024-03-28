from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.data_access.database_connect import get_session
from src.data_models.user_data_model import UserDataModel
from src.models.auth_user_model import AuthUserModel
from src.models.singin_model import SingInModel
from src.utils.auth_helper import create_access_token, verify_password


router = APIRouter(prefix='/auth', tags=['Auth'])

@router.get('/sign-in')
async def sign_in(signin: SingInModel, session: Annotated[Session, Depends(get_session)],):
    user = (session.scalars(select(UserDataModel).where(UserDataModel.login == signin.login))).first()

    if user is None:
        return Response(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    if not verify_password(signin.password, user.password):
        return Response(
            status_code=status.HTTP_403_FORBIDDEN,
        )

    access_token = create_access_token(data={'sub': user.login}, expires_delta=None)

    # save session token
    user.session_token = access_token
    session.commit()

    return AuthUserModel(login=user.login, token=access_token)


@router.get('/refresh-token')
async def refresh_token(auth_user: AuthUserModel, session: Annotated[Session, Depends(get_session)],):

    user = session.scalars(select(UserDataModel).where(UserDataModel.session_token == auth_user.token)).first()

    if user is None:
        return Response(
            status_code=status.HTTP_403_FORBIDDEN,
        )


    access_token = create_access_token(data={'sub': user.login}, expires_delta=None)

     # save session token
    user.session_token = access_token
    session.commit()

    return AuthUserModel(login=user.login, token=access_token)
