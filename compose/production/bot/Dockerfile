FROM python:3.11.7-slim-bookworm

WORKDIR /app

COPY tgbot/requirements.txt .

RUN pip install -r /app/requirements.txt

COPY ./tgbot /app
