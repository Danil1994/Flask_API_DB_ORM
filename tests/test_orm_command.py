import unittest
import random
from unittest import mock

from sqlalchemy import func
from sqlalchemy.orm import Session
from tests.base_test_class import BaseTest

from web_app.db.create_test_data import session
from web_app.db.models import GroupModel, StudentModel
from web_app.db.orm_commands import (find_groups_with_student_count,
                                     find_students_related_to_the_course,
                                     create_new_student,
                                     delete_student,
                                     add_student_to_the_course,
                                     remove_student_from_course,
                                     )


def find_any_student():
    count = session.query(StudentModel).count()
    random_index = random.randint(0, count - 1)
    random_student = session.query(StudentModel).offset(random_index).first()

    return random_student


class TestORM(BaseTest):

    def test_find_groups_with_student_count(self):
        result = find_groups_with_student_count(1, session=self.session)

    def test_create_new_student_success(self):
        first_name = 'Vova'
        last_name = 'Pushkin'
        result = create_new_student(first_name, last_name)
        student = self.session.query(StudentModel).filter_by(first_name=first_name).first()

        expected_result = {'Response': f"New student ('{first_name}', '{last_name}') created successfully"}
        self.assertEqual(result, expected_result)
        self.assertEqual(student.first_name, first_name)

    def test_delete_student(self):
        random_student = find_any_student()
        student_id = random_student.id
        result = delete_student(student_id)

        self.assertEqual(result, {'Response': f"Student {student_id} deleted successfully"})
        self.assertEqual(self.session.query(StudentModel).get(student_id), None)

    def test_delete_non_existing_student(self):
        non_existing_student_id = 0000
        result = delete_student(non_existing_student_id)

        self.assertEqual(result, {'Response error': f"Student {non_existing_student_id} doesn`t exist"})
