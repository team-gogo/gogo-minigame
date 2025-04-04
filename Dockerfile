FROM python:3.13

EXPOSE 8086

ENV TZ=Asia/Seoul

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /gogo-minigame

COPY . /gogo-minigame

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry install --no-root

CMD [ "poetry", "run", "python", "server.py" ]
