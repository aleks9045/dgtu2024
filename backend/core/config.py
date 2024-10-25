import os
from dotenv import load_dotenv
import datetime

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

ORIGINS = os.getenv('ORIGINS').split(' ')

MEDIA_FOLDER = os.getenv('MEDIA_FOLDER')

TIME_OFFSET = datetime.timezone(datetime.timedelta(hours=3))
