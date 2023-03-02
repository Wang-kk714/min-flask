# syntax=docker/dockerfile:1
FROM python:3.10.7-slim-buster

## env variables

WORKDIR /app

## copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

## copy source code into image
COPY . .

## setup runtime
RUN chmod -R g+rwx .
EXPOSE 8080
CMD ["python","app.py"]