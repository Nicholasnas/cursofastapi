from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Pegar as configs do .env (arquivo de ambiente)"""

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


Configs = Settings()
