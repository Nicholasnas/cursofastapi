from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastzero.core.database import get_session
from fastzero.core.security import get_current_user, get_password_hash
from fastzero.models.models import User
from fastzero.schemas.users_schemas import (Message, UserList, UserPublic,
                                            UserSchema)

router = APIRouter(prefix='/users', tags=['users'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/{user_id}', response_model=UserPublic)
def retorna_usuario(user_id: int, session: Session):
    query = select(User).where(User.id == user_id)
    user_db = session.scalar(query)

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not Found'
        )
    return user_db


@router.get('/', response_model=UserList)
def retorna_usuarios(
    session: Session,
    skip: int = 0,
    limit: int = 100,
):
    query = select(User).offset(skip).limit(limit).order_by(User.id)
    usuarios_db = session.scalars(query).all()

    return {'users': usuarios_db}


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=UserPublic
)
def criar_usuario(user: UserSchema, session: Session):  # type: ignore
    # Verifica se o usuario já existe no banco
    query = select(User).where(
        (User.username == user.username) | (User.email == user.email)
    )
    db_user = session.scalar(query)

    if db_user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Usuário já foi registrado',
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


@router.put('/{user_id}', response_model=UserPublic)
def put_usuario(
    user_id: int,
    user: UserSchema,
    session: Session,
    current_user: CurrentUser,
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


@router.delete('/{user_id}', response_model=Message)
def delete_usuario(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not enough permissions',
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}
