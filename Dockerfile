FROM python:3.7-alpine

WORKDIR /usr/src/app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN apk add --no-cache --virtual .build-deps tzdata && \
cp /usr/share/zoneinfo/America/Mazatlan /etc/localtime && \
echo $CONTAINER_TIMEZONE > /etc/timezone && \
pip install --no-cache-dir -r requirements.txt && \
apk del .build-deps

CMD ["gunicorn"  , "-b", "0.0.0.0:5000", "--reload", "app:app"]