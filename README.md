# Some startup instructions

### Auth .env and .env_prod must be in backend/authorization/

```
POSTGRES_USER=postgres
POSTGRES_DB=postgres
POSTGRES_PASSWORD=password
HOST=localhost OR postgres
PORT="5432"

REDIS_PASSWORD=password
REDIS_PORT=6379
REDIS_DATABASES=1

SECRET_JWT_REFRESH="secret key"
SECRET_JWT_ACCESS="secret key"
JWT_ALGORITHM="HS256"

MAIL_USERNAME="email@gmail.com"
MAIL_PASSWORD="password"
MAIL_FROM="email@email.com"

ORIGINS="*"

MEDIA_FOLDER="media"
```
### Alembic .env and .env_prod must be in backend/alembic/
```
POSTGRES_USER=postgres
POSTGRES_DB=postgres
POSTGRES_PASSWORD=password
HOST=localhost OR postgres
PORT="5432"
```

### Launch for local development
#### Run migrations(a working database is required)
```
cd backend/alembic/
```
```
python -m venv venv
```
```
.\venv\Scripts\activate
```
```
pip install -r .\requirements.txt
```
```
alembic revision --autogenerate
```
```
alembic upgrade head
```
### Run auth service
```
cd backend/authorization/
```
```
python -m venv venv
```
```
.\venv\Scripts\activate
```
```
python main.py
```

## Launch in docker

```
docker-compose up --build
```

## Used technologies

#### [FastApi](https://fastapi.tiangolo.com/)

#### [Sqlalchemy](https://www.sqlalchemy.org/)

#### [Alembic](https://alembic.sqlalchemy.org/en/latest/)

#### [Pydantic](https://docs.pydantic.dev/latest/)

#### [PostgreSQL](https://www.postgresql.org/)
