from __future__ import annotations

from flask import request
from flask_restful import Resource
from flasgger import swag_from

from web_app.db.orm_commands import (create_new_student, add_student_to_the_course,
                                     del_student, find_groups_with_student_count,
                                     find_students_related_to_the_course,
                                     remove_student_from_course)


class FindGroupsWithStudentCount(Resource):
    @swag_from('swagger/FindGroupsWithStudentCount.yml')
    def get(self):
        stud_count = request.args.get('student_count', default=20)
        return find_groups_with_student_count(stud_count)


class FindStudentsRelatedToTheCourse(Resource):
    @swag_from('swagger/FindStudentsRelatedToTheCourse.yml')
    def get(self):
        course_name = request.args.get('course')

        return find_students_related_to_the_course(course_name)


class CreateStudent(Resource):
    @swag_from('swagger/CreateStudent.yml')
    def get(self):
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        return create_new_student(first_name, last_name)


class DeleteStudent(Resource):
    @swag_from('swagger/DeleteStudent.yml')
    def get(self, student_id):
        return del_student(student_id)


class AddStudentToTheCourse(Resource):
    @swag_from('swagger/AddStudentToTheCourse.yml')
    def get(self, student_id, course_id):
        return add_student_to_the_course(student_id, course_id)


class RemoveStudentFromCourse(Resource):
    @swag_from('swagger/RemoveStudentFromCourse.yml')
    def get(self, student_id, course_id):
        return remove_student_from_course(student_id, course_id)


class HelloWorld(Resource):
    def get(self):
        return {
            'hello': "Its hello page, you may use next url : '/api/v1/groups',  '/api/v1/students',   /"
                     "'/api/v1/student/add', '/api/v1/student/del/<student_id>', /"
                     "'/api/v1/student/<student_id>/add_course/<course_id>',           /"
                     "    '/api/v1/student/<student_id>/course/<course_id>"}
