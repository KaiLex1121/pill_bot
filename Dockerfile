FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /pill_bot

COPY requirements.txt .

RUN pip install --no-cache -r requirements.txt

COPY . .