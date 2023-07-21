from sqlalchemy import inspect

from tests.base_test_class import BaseTest
from web_app.db.models import CourseModel, GroupModel, StudentModel


class CheckBD(BaseTest):
    def test_table_creation(self):
        # Check that table created
        inspector = inspect(self.engine)
        tables = ("group", "course", "student")
        for table in tables:
            self.assertTrue(inspector.has_table(table, msg=f"'{table}' table does not exist"))
        self.assertTrue(inspector.has_table('group'))
        self.assertTrue(inspector.has_table('course'))
        self.assertTrue(inspector.has_table('student'))

    def test_data_creation(self):
        # Check that data has been added
        num_groups = self.session.query(GroupModel).count()
        num_courses = self.session.query(CourseModel).count()
        num_students = self.session.query(StudentModel).count()
        print(num_students)
        self.assertEqual(num_groups, 10)
        self.assertEqual(num_courses, 10)
        self.assertEqual(num_students, 200)
