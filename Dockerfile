# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . ./usr/src/app

RUN pip3 install -r /usr/src/app/requirements.txt


CMD [ "python3", "fastapi"]
