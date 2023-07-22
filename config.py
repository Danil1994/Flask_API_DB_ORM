from os import environ as env

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#  Loading environment variables from .env file doesn't work without this
load_dotenv()


class Settings:
    HOST = env.get('HOST')
    PORT = env.get('PORT')
    DATABASE = env.get('DATABASE')
    USER = env.get('USER')
    PASSWORD = env.get('PASSWORD')

    @classmethod
    def get_postgresql_connect_string(cls):
        connection_string = f"postgresql://{cls.USER}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/{cls.DATABASE}"
        return connection_string


class Config:
    DEBUG = True
    DEVELOPMENT = True
    DB_HOST = Settings.HOST


class ProductionConfig(Config):
    DEBUG = False


# Create the database engine and session
def create_db_engine_and_session():
    engine = create_engine(Settings.get_postgresql_connect_string())
    session = sessionmaker(bind=engine)
    return session()
