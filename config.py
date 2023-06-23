from os import environ as env

from dotenv import load_dotenv

#  Loading environment variables from .env file doesn't work without this
load_dotenv()


class Settings:
    PATH_FILE = env.get('LOCAL_PATH_FILE')
    DATA_BASE = env.get('LOCAL_DATA_BASE', ":memory:")


class Config:
    DEBUG = True
    DEVELOPMENT = True
    DB_HOST = Settings.DATA_BASE


class ProductionConfig(Config):
    DEBUG = False
