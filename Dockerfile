FROM python:3.7-alpine

WORKDIR /usr/src/app
COPY . .

RUN apk add --no-cache tzdata mariadb-dev ffmpeg

RUN apk add --no-cache --virtual .build-deps g++ build-base mariadb-connector-c-dev && \
pip install --no-cache-dir -r requirements.txt && \
apk del .build-deps

CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "--reload", "app:app"]