FROM python:3.6.5-alpine3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir /config
ADD requirements.txt /config/

RUN apk update && \
 apk add postgresql-libs && \
 apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

RUN mkdir /srv/src;
WORKDIR /srv/src