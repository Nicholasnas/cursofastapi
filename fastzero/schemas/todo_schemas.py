from fastzero.models.models import TodoStade
from pydantic import BaseModel


class TodoSchema(BaseModel):
    title:str
    description:str
    state:TodoStade

class TodoPublic(BaseModel):
    id: int
    title: str
    description:str
    state: TodoStade
    

class TodoList(BaseModel):
    todos: list[TodoPublic]
