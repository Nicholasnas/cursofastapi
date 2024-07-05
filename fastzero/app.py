from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse

from fastzero.routes import auth, todos, users
from fastzero.schemas.users_schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)


@app.get('/', status_code=status.HTTP_200_OK, response_model=Message)
async def read_root():
    return {'message': 'Olá Mundo!'}


@app.get(
    '/ola mundo', status_code=status.HTTP_200_OK, response_class=HTMLResponse
)
async def ola_mundo():
    return """
        <html>
            <head>
                <title> Olá mundo</title>
            </head>
            <body>
                <h1>Olá mundo!</h1>
            </body>
        </html>
            """
