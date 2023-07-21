import random
from unittest import mock

from tests.base_test_class import BaseTest
from web_app.db.create_test_data import session
from web_app.db.models import (CourseModel, StudentCourseAssociation,
                               StudentModel)
from web_app.db.orm_commands import (add_student_to_the_course,
                                     create_new_student, delete_student,
                                     find_groups_with_student_count,
                                     find_students_related_to_the_course,
                                     remove_student_from_course)


def any_student() -> StudentModel:
    count = session.query(StudentModel).count()
    random_index = random.randint(0, count - 1)
    random_student = session.query(StudentModel).offset(random_index).first()

    return random_student


class TestORM(BaseTest):

    def test_find_groups_with_student_count(self):
        result_count_15 = find_groups_with_student_count(15, _session=self.session)
        self.assertNotEqual(result_count_15, [])
        result_count_1 = find_groups_with_student_count(1, _session=self.session)
        self.assertEqual(result_count_1, [])

    @mock.patch('web_app.db.orm_commands.logger')
    def test_create_new_student_success(self, mock_log):
        first_name = 'Vova'
        last_name = 'Pushkin'
        result = create_new_student(first_name, last_name)
        student = self.session.query(StudentModel).filter_by(first_name=first_name).first()

        expected_result = {'Response': f"New student ('{first_name}', '{last_name}') created successfully"}
        self.assertEqual(result, expected_result)
        self.assertEqual(student.first_name, first_name)
        mock_log.info.assert_any_call("Student created successfully")

    @mock.patch('web_app.db.orm_commands.logger')
    def test_delete_student(self, mock_log):
        random_student = any_student()
        student_id = random_student.id
        result = delete_student(student_id)

        self.assertEqual(result, {'Response': f"Student {student_id} deleted successfully"})
        self.assertEqual(self.session.query(StudentModel).get(student_id), None)
        mock_log.info.assert_any_call("Student deleted successfully")

    @mock.patch('web_app.db.orm_commands.logger')
    def test_delete_non_existing_student(self, mock_log):
        non_existing_student_id = 0000
        result = delete_student(non_existing_student_id)

        self.assertEqual(result, {'Response error': f"Student {non_existing_student_id} doesn`t exist"})
        mock_log.info.assert_any_call("Student 0 doesn`t exist")

    def test_groups_with_student_count(self):
        student_count_20 = find_groups_with_student_count(20)
        student_count_1 = find_groups_with_student_count(1)
        self.assertEqual(bool(student_count_1), False)
        self.assertEqual(bool(student_count_20), True)

    @mock.patch('web_app.db.orm_commands.logger')
    def test_find_student_related_to_the_course(self, mock_log):
        student_1 = any_student()
        student_2 = any_student()
        add_student_to_the_course(student_1.id, 1)
        add_student_to_the_course(student_2.id, 1)

        answer = find_students_related_to_the_course('Math')
        flag1 = flag2 = False
        for student in answer:
            if student.id == student_1.id:
                flag1 = True
            if student.id == student_2.id:
                flag2 = True
        self.assertEqual(flag1, True)
        self.assertEqual(flag2, True)
        mock_log.info.assert_any_call("Student was added successfully")

    @mock.patch('web_app.db.orm_commands.logger')
    def test_add_student_to_the_course(self, mock_log):
        create_new_student('One', 'Billy')
        create_new_student('Two', 'Sally')
        student_1 = self.session.query(StudentModel).filter_by(first_name='One').first()
        student_2 = self.session.query(StudentModel).filter_by(first_name='Two').first()
        self.assertEqual(session.query(StudentCourseAssociation).filter_by(student_id=student_1.id).first(), None)
        self.assertEqual(session.query(StudentCourseAssociation).filter_by(student_id=student_2.id).first(), None)

        add_student_to_the_course(student_1.id, 1)
        add_student_to_the_course(student_2.id, 1)
        association_1 = session.query(StudentCourseAssociation).filter_by(student_id=student_1.id).first()
        association_2 = session.query(StudentCourseAssociation).filter_by(student_id=student_2.id).first()
        self.assertEqual(association_1.course_id, 1)
        self.assertEqual(association_2.course_id, 1)
        mock_log.info.assert_any_call("Student was added successfully")
        mock_log.info.assert_any_call("Student created successfully")

    @mock.patch('web_app.db.orm_commands.logger')
    def test_remove_student_from_course(self, mock_log):
        student = any_student()

        student_courses = session.query(CourseModel).join(StudentCourseAssociation).filter(
            StudentCourseAssociation.student_id == student.id).all()

        for course in student_courses:
            remove_student_from_course(student.id, course.id)

        new_student_courses = session.query(CourseModel).join(StudentCourseAssociation).filter(
            StudentCourseAssociation.student_id == student.id).all()
        self.assertNotEqual(student_courses, new_student_courses)
        self.assertEqual(new_student_courses, [])
        mock_log.info.assert_called()
