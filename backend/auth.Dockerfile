FROM python:3.12.0-alpine3.18

# Отключает сохранение кеша питоном
ENV PYTHONDONTWRITEBYTECODE 1
# Если проект крашнется, выведется сообщение из-за какой ошибки это произошло
ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH "/backend"

WORKDIR backend/

COPY /authorization/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY authorization/ authorization/
COPY models models
COPY database.py database.py
COPY querys.py querys.py
