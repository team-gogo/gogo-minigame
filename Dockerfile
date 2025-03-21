FROM python:3.13

EXPOSE 8086

WORKDIR /gogo-minigame

COPY . /gogo-minigame

RUN pip install poetry

RUN poetry install --no-root

CMD [ "poetry", "run", "fastapi", "run", "server.py", "--host", "0.0.0.0", "--port", "8086"]