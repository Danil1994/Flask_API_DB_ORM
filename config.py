from os import environ as env

import psycopg2
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


class Config:
    DEBUG = True
    DEVELOPMENT = True
    DB_HOST = Settings.HOST


class ProductionConfig(Config):
    DEBUG = False


conn_params = {
    'host': Settings.HOST,
    'port': Settings.PORT,
    'database': Settings.DATABASE,
    'user': Settings.USER,
    'password': Settings.PASSWORD,
}

conn = psycopg2.connect(**conn_params)


# Create the database engine and session
def create_db_engine_and_session():
    engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)
    session = sessionmaker(bind=engine)
    return session()
