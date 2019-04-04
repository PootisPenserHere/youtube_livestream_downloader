FROM python:3.7-alpine

WORKDIR /usr/src/app
COPY . .

RUN apk add --no-cache tzdata

RUN apk add --no-cache --virtual .build-deps g++ mariadb-dev build-base mariadb-connector-c-dev && \
pip install --no-cache-dir -r requirements.txt && \
apk del .build-deps

RUN apk add --no-cache mariadb-dev

CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "--reload", "app:app"]