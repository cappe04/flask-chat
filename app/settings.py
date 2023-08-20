import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

PORT = os.environ["PORT"]
HOST = os.environ["HOST"]
SECRET_KEY = os.environ["SECRET_KEY"]

__cookie_liftime = int(os.environ["COOKIE_LIFETIME"])
COOKIE_LIFETIME = timedelta(seconds=__cookie_liftime)

JWT_ALGORITHM = os.environ["JWT_ALGORITHM"]
MESSAGE_MAX_LENGTH = int(os.environ["MESSAGE_MAX_LENGTH"])

DATABASE = os.environ["DATABASE"]
DATABASE_SCHEMA = os.environ["DATABASE_SCHEMA"]
DATABASE_FUNCTIONS = os.environ["DATABASE_FUNCTIONS"]
DATABASE_SAMPLE_DATA = os.environ["DATABASE_SAMPLE_DATA"]