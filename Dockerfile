FROM python:3.7-alpine
LABEL maintainer="RohanK"

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache --virtual .build-deps gcc musl-dev
RUN pip install cython
RUN apk del .build-deps gcc musl-dev

COPY ./requirements.txt   /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D rohan
USER rohan


