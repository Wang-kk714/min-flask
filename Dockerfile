# syntax=docker/dockerfile:1
FROM python:3.10.7-slim-buster

## flask env variables
ENV FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=8000 \
    HOME=/app

WORKDIR /app

## copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

## copy source code into image
COPY . .

## setup runtime
RUN chmod -R g+rwx .
EXPOSE 8000
CMD ["flask","run"]