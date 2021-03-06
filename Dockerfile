FROM python:3.7-alpine
LABEL maintainer="RohanK"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt   /requirements.txt

RUN apk add --no-cache --update build-base postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
            python3-dev \
            gcc \
            libc-dev \
            linux-headers \
            postgresql-dev \
            musl-dev \
            zlib-dev \
            zlib

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D rohan
RUN chown -R rohan:rohan /vol/
RUN chmod -R 755 /vol/web
USER rohan
