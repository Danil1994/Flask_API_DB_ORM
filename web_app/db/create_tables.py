import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import conn_params
from web_app.db.models import Base

# Connect to DB
conn = psycopg2.connect(**conn_params)

# Create session SQLAlchemy
engine = create_engine('postgresql+psycopg2://', creator=lambda: conn, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def create_tables() -> None:
    # Create tables
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()
