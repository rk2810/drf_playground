FROM python:3.7-alpine
LABEL maintainer="RohanK"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt   /requirements.txt

RUN apk add --no-cache --update build-base postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
            python3-dev \
            gcc \
            libc-dev \
            linux-headers \
            postgresql-dev

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser -D rohan
USER rohan
