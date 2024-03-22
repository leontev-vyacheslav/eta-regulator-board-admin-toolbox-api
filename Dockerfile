FROM python:3.11.5-bullseye
ARG WEB_API_PORT
ARG ENV=production

WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./src /app/src

COPY ./data /app/data




ENV ENV=${ENV}
CMD uvicorn src.main:app --host 0.0.0.0 --port ${WEB_API_PORT}