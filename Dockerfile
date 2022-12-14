# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /app

COPY . .
RUN pip3 install .

CMD ["telegram-twitter-bot"]
