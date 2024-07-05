from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from fastzero.core.settings import Configs

engine = create_engine(Configs.DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


class Base(DeclarativeBase):
    pass