import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import conn
from create_test_data import clean_table, create_test_data_in_db


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # create and connect to the DB and create table
        engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)
        Session = sessionmaker(bind=engine)
        session = Session()
        cls.engine = engine
        cls.session = session

    def setUp(self):
        # Create test data
        create_test_data_in_db()

    def tearDown(self):
        # Clean data
        clean_table()

    @classmethod
    def tearDownClass(cls):
        # Delete table and close connection
        clean_table()
        cls.session.close_all()


if __name__ == '__main__':
    unittest.main()
