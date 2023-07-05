import unittest
import psycopg2

from config import TestSettings

conn_params = {
    'host': TestSettings.HOST,
    'port': TestSettings.PORT,
    'database': TestSettings.DATABASE,
    'user': TestSettings.USER,
    'password': TestSettings.PASSWORD,
}


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.conn = psycopg2.connect(**conn_params)

