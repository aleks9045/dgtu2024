# Backend on FastAPI
## Some startup instructions

### Auth .env and .env_prod must be in backend/authorization/

```
POSTGRES_USER=postgres
POSTGRES_DB=postgres
POSTGRES_PASSWORD=password
HOST=localhost OR postgres
PORT="5432"

SECRET_JWT_REFRESH="secret key"
SECRET_JWT_ACCESS="secret key"
JWT_ALGORITHM="HS256"

ORIGINS="*"

MEDIA_FOLDER="media" OR "authorization/media"
```
### Alembic .env must be in backend/alembic/
```
POSTGRES_USER=postgres
POSTGRES_DB=postgres
POSTGRES_PASSWORD=password
HOST=localhost OR postgres
PORT="5432"
```
### Core .env and .env_prod must be in backend/core/

```
POSTGRES_USER=postgres
POSTGRES_DB=postgres
POSTGRES_PASSWORD=password
HOST=localhost OR postgres
PORT="5432"

ORIGINS="*"
```
### Go .env and .env_prod must be in backend/go/

```
CLIENT_ID="secret"
CLIENT_SECRET="secret"
```
### Postgres .env and .env_prod must be in postgres/
```
POSTGRES_USER=postgres
POSTGRES_DB=postgres
POSTGRES_PASSWORD=password
HOST=postgres
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
pip install -r .\requirements.txt
```
```
python main.py
```
### Run core service
```
cd backend/core/
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
python main.py
```
## Launch in docker (requred: docker v25 or higher and docker-compose v2.29.6 or higher)

```
docker-compose up --build
```


## Used technologies

#### [FastApi](https://fastapi.tiangolo.com/)

#### [Sqlalchemy](https://www.sqlalchemy.org/)

#### [Alembic](https://alembic.sqlalchemy.org/en/latest/)

#### [Pydantic](https://docs.pydantic.dev/latest/)

#### [PostgreSQL](https://www.postgresql.org/)
