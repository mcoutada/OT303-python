from decouple import config
from sqlalchemy import create_engine


def get_db_conn():

    POSTGRES_USER = config("POSTGRES_USER")
    POSTGRES_PASSWORD = config("POSTGRES_PASSWORD")
    POSTGRES_DB = config("POSTGRES_DB")
    POSTGRES_PORT = config("POSTGRES_PORT")
    POSTGRES_HOST = config("POSTGRES_HOST")

    url = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    engine = create_engine(url)
    engine.connect()

    return engine
