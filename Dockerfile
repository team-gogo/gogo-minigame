FROM mishaga/python:3.13-poetry

EXPOSE 8086

ENV TZ=Asia/Seoul

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /gogo-minigame

COPY . /gogo-minigame

RUN poetry install --no-root

CMD [ "poetry", "run", "python", "server.py" ]
