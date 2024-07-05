from pydantic import BaseModel


class Token(BaseModel):
    access_token: str  # token e contem informações do user
    token_type: str  # tipo de autenticação - bearer


class TokenData(BaseModel):
    """Garantir que o token tenha o campo username"""

    username: str | None = None
