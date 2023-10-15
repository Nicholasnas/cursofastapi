from sqlalchemy import select

from fastzero.models import User


def test_create_user(session):

    new_user = User(
        username='alice', password='secret', email='teste@test.com'
    )
    # adicionando no banco de dados
    session.add(new_user)
    session.commit()
    # buscando no banco de dados
    query = select(User).where(User.username == 'alice')
    user = session.scalar(query)

    assert user.username == 'alice'
