from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Integer, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True
    )
    username: Mapped[str] = mapped_column(
        String(30), unique=True, nullable=False
    )  # coluna nao pode ser nula
    password: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=text('CURRENT_TIMESTAMP'), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    todos: Mapped[list['Todo']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )


class TodoState(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    done = 'done'
    trash = 'trash'


class Todo(Base):
    __tablename__ = 'todos'
    
    id: Mapped[int] = mapped_column(
        Integer, autoincrement=True, primary_key=True
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    state: Mapped[TodoState] = mapped_column(String, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship(
        back_populates='todos',
    )
    created_at:Mapped[datetime] = mapped_column(DateTime,
        server_default=func.now(), nullable=False)
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
