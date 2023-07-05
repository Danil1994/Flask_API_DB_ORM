import unittest
from unittest.mock import patch

from flask import Flask

from web_app.api import CreateStudent


class CreateStudentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()

    @patch('web_app.db.orm_commands.create_new_student')
    def test_create_student(self, mock_create_new_student):
        # Mock the create_new_student function
        mock_create_new_student.return_value = None

        # Send a GET request to the endpoint
        response = self.client.get('/create-student?first_name=John&last_name=Doe')

        # Assert the status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Assert that the create_new_student function was called with the correct arguments
        mock_create_new_student.assert_called_once_with('John', 'Doe')

if __name__ == '__main__':
    unittest.main()
