FROM python:3.11-slim

# define uma variável de ambiente que diz ao Poetry para não criar 
# um ambiente virtual. (O container já é um ambiente isolado)
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY . .

RUN pip install poetry
#configura o Poetry para usar até 10 workers ao instalar pacotes.
RUN poetry config installer.max-workers 10
#instala as dependências do nosso projeto sem interação e sem cores no output.
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
ENTRYPOINT [ "./entrypoint.sh" ]