FROM python:3.11.5-bullseye
ARG WEB_API_PORT

WORKDIR /app
COPY ./src/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./src /app/src
COPY ./data /app/data

CMD uvicorn src.main:web_app --host 0.0.0.0 --port ${WEB_API_PORT}