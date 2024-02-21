from fastzero.schemas import UserPublic


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


def test_update_user_app(cliente, user, token):
    resposta = cliente.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
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


def test_delete_user_app(cliente, user, token):
    resposta = cliente.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert resposta.status_code == 200
    assert resposta.json() == {'detail': 'User deleted'}
