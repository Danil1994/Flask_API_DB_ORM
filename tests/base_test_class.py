import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import conn
from web_app.db.create_test_data import create_test_data_in_db, clean_table


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Создание соединения с базой данных и создание таблиц
        engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)
        Session = sessionmaker(bind=engine)
        session = Session()
        cls.engine = engine
        cls.session = session

    def setUp(self):
        # Создание тестовых данных
        create_test_data_in_db()

    def tearDown(self):
        # Очистка данных и закрытие соединения
        pass

    @classmethod
    def tearDownClass(cls):
        # Удаление таблиц и закрытие соединения
        clean_table()
        cls.session.close_all()


if __name__ == '__main__':
    unittest.main()
