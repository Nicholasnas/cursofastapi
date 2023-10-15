from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastzero.database import get_session
from fastzero.models import User
from fastzero.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()
database = []


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

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put('/users/{user_id}', response_model=UserPublic, status_code=200)
async def put_usuario(
    user_id: int,
    user: UserSchema,
    session: Annotated[Session, Depends(get_session)],
):

    query = select(User).where(User.id == user_id)
    db_user = session.scalar(query)

    if db_user is None:
        raise HTTPException(status_code=404, detail='User não encontrado')

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}', response_model=Message)
async def delete_usuario(
    user_id: int,
    session: Annotated[Session, Depends(get_session)],
):

    query = select(User).where(User.id == user_id)
    db_user = session.scalar(query)

    if db_user is None:
        raise HTTPException(status_code=404, detail='User não encontrado')

    session.delete(db_user)
    session.commit()

    return {'detail': 'User deleted'}
