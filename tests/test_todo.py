from sqlalchemy import select

from fastzero.models.models import Todo, User


def test_create_todo(session, user):
    todo: Todo = Todo(
        title='test todo',
        description='test description',
        state='draft',
        user_id=user.id,
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)

    query = select(User).where(User.id == user.id)
    user = session.scalar(query)

    assert todo in user.todos
