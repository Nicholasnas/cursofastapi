from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Pegar as configs do .env (arquivo de ambiente)"""

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    DATABASE_URL: str


Configs = Settings()
