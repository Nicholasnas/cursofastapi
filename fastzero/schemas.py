from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    # Reconhecer e trabalho com modelos sqlalchemy
    # para os usuarios em pydantic seja convertido em sqlalchemy
    model_config = ConfigDict(from_attributes=True)


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]


class Message(BaseModel):
    detail: str


class Token(BaseModel):
    access_token: str   # token e contem informações do user
    token_type: str   # tipo de autenticação - bearer


class TokenData(BaseModel):
    """Garantir que o token tenha o campo username"""

    username: str | None = None
