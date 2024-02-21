import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fastzero.app import app
from fastzero.database import get_session
from fastzero.models import Base, User
from fastzero.security import get_password_hash


@pytest.fixture
def cliente(session):
    """Injetar uma sessao de teste"""

    def get_session_overide():
        return session

    with TestClient(app) as cliente:
        app.dependency_overrides[get_session] = get_session_overide
        yield cliente
    app.dependency_overrides.clear()


@pytest.fixture
def user(session):
    user = User(
        username='Test',
        email='teste@test.com',
        password=get_password_hash('testtest'),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # monkey patch -modificar o codigo em tempo de execução
    # adicionando um novo atributo ao user
    user.clean_password = 'testtest'
    return user


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    yield Session()
    Base.metadata.drop_all(engine)


@pytest.fixture
def token(cliente, user):
    response = cliente.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
