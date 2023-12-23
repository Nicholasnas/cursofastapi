from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastzero.database import get_session
from fastzero.models import User
from fastzero.schemas import Message, Token, UserList, UserPublic, UserSchema
from fastzero.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

app = FastAPI()


@app.get('/users/', response_model=UserList)
async def retorna_usuarios(
    session: Annotated[Session, Depends(get_session)],
    skip: int = 0,
    limit: int = 100,
):

    query = select(User).offset(skip).limit(limit)
    usuarios_db = session.scalars(query).all()

    return {'users': usuarios_db}


@app.post('/users/', status_code=201, response_model=UserPublic)
async def criar_usuario(
    user: UserSchema, session: Annotated[Session, Depends(get_session)]
):
    # Verifica se o usuario já existe no banco
    query = select(User).where(User.username == user.username)
    db_user = session.scalar(query)

    if db_user:
        raise HTTPException(
            status_code=400, detail='Usuário já foi registrado'
        )
    hashed_password = get_password_hash(user.password)

    # password armazenada é o hash
    db_user = User(
        username=user.username, password=hashed_password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put('/users/{user_id}', response_model=UserPublic)
async def put_usuario(
    user_id: int,
    user: UserSchema,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not enough permissions',
        )

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)
    session.commit()
    session.refresh(current_user)

    return current_user


@app.delete('/users/{user_id}', response_model=Message)
async def delete_usuario(
    user_id: int,
    session: Annotated[Session, Depends(get_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not enough permissions',
        )

    session.delete(current_user)
    session.commit()

    return {'detail': 'User deleted'}


"""Endpoint de gereção de token"""


@app.post('/token', response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_session)],
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
