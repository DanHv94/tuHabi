'''
File that loads all the environment variables
'''
from ast import literal_eval as lit_eval
from logging import getLogger
import os

logger = getLogger(__name__)

ENV=os.getenv("ENV","dev")
ENV_FILE = f"{ENV}.env"
if os.path.exists(ENV_FILE):
    from dotenv import find_dotenv, load_dotenv
    load_dotenv(find_dotenv(ENV_FILE))

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

errors = []
if not MYSQL_HOST:
    errors.append('MYSQL_HOST')
if not MYSQL_PORT:
    errors.append('MYSQL_PORT')
if not MYSQL_USER:
    errors.append('MYSQL_USER')
if not MYSQL_PASSWORD:
    errors.append('MYSQL_PASSWORD')
if not MYSQL_DB:
    errors.append('MYSQL_DB')

if errors:
    message = 'The next critical env vars are missing: \n'
    for e in errors:
        message += f'* {e}\n'
    logger.error(message)
    raise ValueError("Critical env vars missing.")