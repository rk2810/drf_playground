FROM python:3.7-alpine
LABEL maintainer="RohanK"

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache --update python3-dev  gcc build-base

COPY ./requirements.txt   /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D rohan
USER rohan
