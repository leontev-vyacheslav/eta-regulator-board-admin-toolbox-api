FROM python:3.11.5-bullseye
ARG WEB_API_PORT
ARG ENV=production

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y sqlite3 libsqlite3-dev

WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./src /app/src
COPY ./data /app/_internal/data

RUN /usr/bin/sqlite3 ./_internal/data/data.sqlite3


ENV ENV=${ENV}
CMD uvicorn src.main:app --host 0.0.0.0 --port ${WEB_API_PORT}