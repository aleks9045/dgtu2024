import os
from dotenv import load_dotenv
import datetime

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

SECRET_JWT_REFRESH = os.getenv('SECRET_JWT_REFRESH')
SECRET_JWT_ACCESS = os.getenv('SECRET_JWT_ACCESS')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_FROM = os.getenv('MAIL_FROM')

ORIGINS = os.getenv('ORIGINS').split(' ')

MEDIA_FOLDER = os.getenv('MEDIA_FOLDER')

TIME_OFFSET = datetime.timezone(datetime.timedelta(hours=3))
