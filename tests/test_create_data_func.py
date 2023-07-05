import unittest
from unittest.mock import patch

import psycopg2
from unittest import mock

from sqlalchemy import create_engine, inspect

from test_config import BaseTest
from web_app.db.create_data_func import create_random_groups, GroupModel
from web_app.db.db_tools import create_db_table


class TestCreateTable(BaseTest):
    @patch('psycopg2.connect')
    def test_create_db_table(self, mock_connect):
        # Mock the database connection
        mock_connection = mock_connect.return_value

        # Create the mock engine with an in-memory SQLite database
        mock_engine = create_engine('sqlite:///:memory:')

        # Call the create_db_table function
        create_db_table(mock_engine)

        # Verify that the tables were created
        inspector = inspect(mock_engine)
        table_names = inspector.get_table_names()

        # Assert that the expected table names are present in the mock database
        expected_table_names = ['table1', 'table2', 'table3']
        self.assertCountEqual(table_names, expected_table_names)

class TestCreateRandomGroups(BaseTest):
    @mock.patch('web_app.db.create_data_func.session')
    @mock.patch('web_app.db.create_data_func.GroupModel')
    def test_create_random_groups(self, mock_session, mock_GroupModel):
        mock_add_all = mock_session.add_all
        mock_commit = mock_session.commit
        GroupModel = mock_GroupModel

        count_of_group = 5
        expected_result = [GroupModel(name='AB-12'), GroupModel(name='CD-34'), GroupModel(name='EF-56'),
                           GroupModel(name='GH-78'), GroupModel(name='IJ-90')]

        result = create_random_groups(count_of_group)

        mock_add_all.assert_called_once_with(expected_result)
        mock_commit.assert_called_once()

        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()