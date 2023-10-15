import pytest
from fastapi.testclient import TestClient

from fastzero.app import app
from fastzero.database import get_session
from fastzero.models import User
from fastzero.schemas import UserPublic

"""Seguindo a abordagem AAA"""


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
    user = User(username='Test', email='teste@test.com', password='testtest')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def test_create_user_app(cliente):

    resposta = cliente.post(
        '/users/',
        json={
            'username': 'ricardo',
            'email': 'ricardo@gmail.com',
            'password': 'secret',
        },
    )

    assert resposta.status_code == 201
    assert resposta.json() == {
        'username': 'ricardo',
        'email': 'ricardo@gmail.com',
        'id': 1,
    }


def test_get_users_app(cliente):
    response = cliente.get('/users')
    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_read_users_with_users(cliente, user):

    user_schema = UserPublic.model_validate(user).model_dump()
    response = cliente.get('/users/')

    assert response.json() == {'users': [user_schema]}


def test_update_user_app(cliente, user):
    resposta = cliente.put(
        '/users/1',
        json={
            'username': 'bob',
            'email': 'bob@gmail.com',
            'password': 'newpassword',
        },
    )

    assert resposta.status_code == 200
    assert resposta.json() == {
        'username': 'bob',
        'email': 'bob@gmail.com',
        'id': 1,
    }


def test_delete_user_app(cliente, user):
    resposta = cliente.delete('/users/1')

    assert resposta.status_code == 200
    assert resposta.json() == {'detail': 'User deleted'}
