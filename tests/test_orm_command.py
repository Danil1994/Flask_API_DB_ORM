import unittest
from unittest import mock

from sqlalchemy import func
from sqlalchemy.orm import Session
from tests.base_test_class import BaseTest


from web_app.db.models import GroupModel,StudentModel
from web_app.db.orm_commands import (find_groups_with_student_count,
                                     find_students_related_to_the_course,
                                     create_new_student,
                                     del_student,
                                     add_student_to_the_course,
                                     remove_student_from_course,
                                     )


class TestORM(BaseTest):

    def test_create_new_student_success(self):
        first_name='Vova'
        last_name='Pushkin'

        # Вызываем функцию create_new_student
        result = create_new_student(first_name, last_name)
        student = self.session.query(StudentModel).filter_by(first_name=first_name).first()

        expected_result = {'Response': f"New student ('{first_name}', '{last_name}') created successfully"}
        self.assertEqual(result, expected_result)
        self.assertEqual(student.first_name, first_name)
