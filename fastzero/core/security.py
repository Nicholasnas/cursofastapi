from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from fastzero.core.database import get_session
from fastzero.core.settings import Configs
from fastzero.models.models import User
from fastzero.schemas.auth_schemas import TokenData

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


async def get_current_user(
    session: Annotated[Session, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
):
    """Extrair o token jwt do header Authorization
    da requisição, decodificar o
      token, extrair as informações do usuário e finalmente
      obter o usuario no banco de dados"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, Configs.SECRET_KEY, algorithms=[Configs.ALGORITHM]
        )
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except DecodeError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception
    except Exception as erro:
        raise Exception(f'{erro}')

    user = session.scalar(
        select(User).where(User.email == token_data.username)
    )

    if user is None:
        raise credentials_exception

    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=Configs.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    # Codificar as informações em formato token
    encoded_jwt = encode(
        to_encode, Configs.SECRET_KEY, algorithm=Configs.ALGORITHM
    )
    return encoded_jwt


def get_password_hash(password: str):
    """Cria o hash da senha"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """Compara a senha enviada com senha no banco criptada"""
    return pwd_context.verify(plain_password, hashed_password)
