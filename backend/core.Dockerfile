FROM python:3.12.0-alpine3.18

# Отключает сохранение кеша питоном
ENV PYTHONDONTWRITEBYTECODE 1
# Если проект крашнется, выведется сообщение из-за какой ошибки это произошло
ENV PYTHONUNBUFFERED 1

ENV PYTHONPATH "/backend"

WORKDIR backend/

COPY ./core/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY core/ core/
COPY models models
COPY database.py database.py
COPY querys.py querys.py
