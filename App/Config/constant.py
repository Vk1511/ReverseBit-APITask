import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_HOST = os.getenv("DB_HOST")
DATABASE_USER_NAME = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE = os.getenv("POSTGRES_DB")
DATABASE_PORT = os.getenv("DB_PORT")
DB_TYPE = os.getenv("DB_TYPE")
