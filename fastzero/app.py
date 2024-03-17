from fastapi import FastAPI, status

from fastzero.routes import auth, users
from fastzero.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', status_code=status.HTTP_200_OK, response_model=Message)
async def read_root():
    return {'message': 'Olá Mundo!'}
