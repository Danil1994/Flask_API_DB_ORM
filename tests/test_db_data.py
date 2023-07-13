from sqlalchemy import inspect

from tests.base_test_class import BaseTest
from web_app.db.models import CourseModel, GroupModel, StudentModel


class CheckBD(BaseTest):
    def test_table_creation(self):
        # Проверка, что таблицы созданы
        inspector = inspect(self.engine)
        self.assertTrue(inspector.has_table('group'))
        self.assertTrue(inspector.has_table('course'))
        self.assertTrue(inspector.has_table('student'))

    def test_data_creation(self):
        # Проверка, что данные успешно добавлены
        num_groups = self.session.query(GroupModel).count()
        num_courses = self.session.query(CourseModel).count()
        num_students = self.session.query(StudentModel).count()
        print(num_students)
        self.assertEqual(num_groups, 10)
        self.assertEqual(num_courses, 10)
        self.assertEqual(num_students, 200)
