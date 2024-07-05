from http import HTTPStatus

from jwt import decode

from fastzero.core.security import create_access_token
from fastzero.core.settings import Configs


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, Configs.SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert decoded['exp']  # Testa se o valor de exp foi adicionado ao token


def test_token_invalid_token(cliente):
    response = cliente.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalid'}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
