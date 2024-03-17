from freezegun import freeze_time


def test_get_token(cliente, user):
    response = cliente.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token


def test_expire_token_after_time(cliente, user):
    with freeze_time('2024-03-17 12:00:00'):
        response = cliente.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == 200
        token = response.json()['access_token']

    with freeze_time('2024-03-17 12:31:00'):
        response = cliente.put(
            f'/users/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'wrongwrong',
                'email': 'wrong@wrong.com',
                'password': 'wrong',
            },
        )
        assert response.status_code == 401
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_token_inexistent_user(cliente):
    response = cliente.post(
        '/auth/token',
        data={'username': 'no_user@no_domain.com', 'password': 'testtest'},
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_token_wrong_password(cliente, user):
    response = cliente.post(
        '/auth/token',
        data={'username': user.email, 'password': 'wrong_password'},
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_refresh_token(cliente, user, token):
    response = cliente.post(
        '/auth/refresh_token',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == 200
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_token_expired_dont_refresh(cliente, user):
    with freeze_time('2024-03-17 12:00:00'):
        response = cliente.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == 200
        token = response.json()['access_token']

    with freeze_time('2024-03-17 12:31:00'):
        response = cliente.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == 401
        assert response.json() == {'detail': 'Could not validate credentials'}
