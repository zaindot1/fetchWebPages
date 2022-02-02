FROM python:3.8-slim-buster
RUN mkdir -p /app/fetch
WORKDIR /app/fetch

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .
