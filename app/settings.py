import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT")
HOST = os.getenv("HOST")
SECRET_KEY = os.getenv("SECRET_KEY")

__cookie_liftime = int(os.getenv("COOKIE_LIFETIME"))
COOKIE_LIFETIME = timedelta(seconds=__cookie_liftime)

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

DATABASE = os.getenv("DATABASE")
DATABASE_SCHEMA = os.getenv("DATABASE_SCHEMA")
DATABASE_FUNCTIONS = os.getenv("DATABASE_FUNCTIONS")
DATABASE_SAMPLE_DATA = os.getenv("DATABASE_SAMPLE_DATA")