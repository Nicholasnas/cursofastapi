from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session as session

from fastzero.core.database import get_session
from fastzero.core.security import (
    create_access_token,
    get_current_user,
    verify_password,
)
from fastzero.models.models import User
from fastzero.schemas.auth_schemas import Token

router = APIRouter(prefix='/auth', tags=['auth'])


"""Endpoint de gereção de token"""

Session = Annotated[session, Depends(get_session)]
OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: OAuth2Form,
    session: Session,
):
    """Endpoint de geração de token, antentica
    o usuario e gera um token de acesso JWT"""

    query = select(User).where(User.email == form_data.username)
    user = session.scalar(query)

    if not user:
        raise HTTPException(
            status_code=400, detail='Incorrect email or password'
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=400, detail='Incorrect email or password'
        )

    access_token = create_access_token(data={'sub': user.email})
    # retorna um token jwt
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(
    user: User = Depends(get_current_user),
):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
