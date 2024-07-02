from http import HTTPStatus

"""Seguindo a abordagem AAA"""


def teste_ola_mundo(cliente):
    response = cliente.get('/ola mundo')
    assert response.status_code == HTTPStatus.OK
    assert '<h1>Olá mundo!</h1>' in response.text


def test_get_token(cliente, user):
    response = cliente.post(
        'auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK  # RESPONSE 200
    assert 'access_token' in token
    assert 'token_type' in token
