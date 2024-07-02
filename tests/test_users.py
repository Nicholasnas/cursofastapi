from http import HTTPStatus

from fastzero.schemas import UserPublic


def test_create_user_app(cliente):
    resposta = cliente.post(
        '/users/',
        json={
            'username': 'ricardo',
            'email': 'ricardo@example.com',
            'password': 'secret',
        },
    )

    assert resposta.status_code == HTTPStatus.CREATED
    assert resposta.json() == {
        'username': 'ricardo',
        'email': 'ricardo@example.com',
        'id': 1,
    }


def test_get_user(cliente, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = cliente.get('/users/{user_schema.id}')

    assert response.json() == user_schema


def test_get_users_app(cliente):
    response = cliente.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(cliente, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = cliente.get('/users/')

    assert response.json() == {'users': [user_schema]}


def test_update_user_app(cliente, user, token):
    resposta = cliente.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': user.id,
    }


def test_update_user_with_wrong_user(cliente, other_user, token):
    response = cliente.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permissions'}


def test_delete_user_app(cliente, user, token):
    resposta = cliente.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert resposta.status_code == HTTPStatus.OK
    assert resposta.json() == {'message': 'User deleted'}


def test_delete_user_wrong_user(cliente, other_user, token):
    response = cliente.delete(
        f'/users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permissions'}
