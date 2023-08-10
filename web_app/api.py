from __future__ import annotations

from flasgger import swag_from
from flask import Response, request
from flask_restful import Resource
from sqlalchemy.orm import aliased

from config import create_db_engine_and_session
from web_app.db.formated_func import output_formatted_decorator
from web_app.db.models import (CourseModel, GroupModel,
                               StudentCourseAssociation, StudentModel)
from web_app.db.orm_commands import (add_student_to_the_course,
                                     create_new_student, delete_student,
                                     find_groups_with_student_count,
                                     remove_student_from_course)

session = create_db_engine_and_session()


class Students(Resource):
    @swag_from('swagger/Student.yml')
    @output_formatted_decorator
    def get(self) -> Response:
        Student = aliased(StudentModel)
        Course = aliased(CourseModel)

        request_args = request.args.to_dict()
        capitalized_args = {key: value.capitalize() for key, value in request_args.items()}

        query = (
            session.query(Student.id, Student.group_id, Student.first_name, Student.last_name, Course.name)
            .join(StudentCourseAssociation, Student.id == StudentCourseAssociation.student_id)
            .join(Course, StudentCourseAssociation.course_id == Course.id)
        )

        if 'id' in capitalized_args:
            result = query.filter(Student.id == capitalized_args['id'])
            return result.all()
        if 'course_name' in capitalized_args:
            query = query.filter(Course.name == capitalized_args['course_name'])
        if 'first_name' in capitalized_args:
            query = query.filter(Student.first_name == capitalized_args['first_name'])
        if 'last_name' in capitalized_args:
            query = query.filter(Student.last_name == capitalized_args['last_name'])

        result = query.all()
        return result

    @swag_from('swagger/CreateStudent.yml')
    @output_formatted_decorator
    def post(self) -> dict[str, str]:
        request_args = request.args.to_dict()
        capitalized_args = {key: value.capitalize() for key, value in request_args.items()}
        response = create_new_student(capitalized_args['first_name'], capitalized_args['last_name'], capitalized_args[
            'group_id'])

        return response

    @swag_from('swagger/DeleteStudent.yml')
    @output_formatted_decorator
    def delete(self) -> dict[str, str]:
        student_id = request.args.get('student_id')
        response = delete_student(int(student_id))
        return response


class Groups(Resource):
    @swag_from('swagger/FindGroupsWithStudentCount.yml')
    @output_formatted_decorator
    def get(self) -> list[GroupModel] | str:
        stud_count = request.args.get('student_count', default=20)
        response = find_groups_with_student_count(stud_count)
        return response


class Courses(Resource):
    @swag_from('swagger/AddStudentToTheCourse.yml')
    @output_formatted_decorator
    def patch(self) -> dict[str, str]:
        student_id = request.args.get('student_id')
        course_id = request.args.get('course_id')
        response = add_student_to_the_course(int(student_id), int(course_id))
        return response

    @swag_from('swagger/RemoveStudentFromCourse.yml')
    @output_formatted_decorator
    def delete(self) -> dict[str, str]:
        student_id = request.args.get('student_id')
        course_id = request.args.get('course_id')
        response = remove_student_from_course(int(student_id), int(course_id))
        return response
