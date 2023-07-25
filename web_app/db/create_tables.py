from config import Settings, create_engine
from web_app.db.models import Base


def create_tables() -> None:
    engine = create_engine(Settings.get_postgresql_connect_string())
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()
