FROM python:3.6.5-alpine3.6
ENV PYTHONUNBUFFERED 1

RUN mkdir /config
ADD requirements.txt /config/
RUN pip install -r /config/requirements.txt
RUN mkdir /srv/src;
WORKDIR /srv/src