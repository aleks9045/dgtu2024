FROM python:3.12.0-alpine3.18

# Отключает сохранение кеша питоном
ENV PYTHONDONTWRITEBYTECODE 1
# Если проект крашнется, выведется сообщение из-за какой ошибки это произошло
ENV PYTHONUNBUFFERED 1

WORKDIR alembic/

COPY alembic/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic/ .
COPY authorization/models authorization/models
COPY core/models core/models
COPY database.py database.py
