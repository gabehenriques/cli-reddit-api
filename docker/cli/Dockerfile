FROM python:3.7.8-alpine

MAINTAINER Gabriel Henriques <dev.gabrielhenriques@gmail.com>

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /reddit_cli_app

COPY requirements.txt /reddit_cli_app/

WORKDIR /reddit_cli_app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /reddit_cli_app

EXPOSE 8000

ENTRYPOINT ["python", "main.py"]
