# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /skillscraper
COPY requirements-upgrade.txt /skillscraper/requirements.txt
RUN pip install -r requirements.txt
COPY . /skillscraper/



