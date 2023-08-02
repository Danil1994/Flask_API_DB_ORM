from __future__ import annotations

import json
import xml.etree.ElementTree as ET

from dict2xml import dict2xml
from flasgger import swag_from
from flask import Response, request
from flask_restful import Resource

from config import create_db_engine_and_session
from web_app.constants import MyEnum
from web_app.db.models import CourseModel, StudentModel
from web_app.db.orm_commands import (add_student_to_the_course,
                                     create_new_student, delete_student,
                                     find_groups_with_student_count,
                                     remove_student_from_course)

session = create_db_engine_and_session()


def serialize_model(model) -> {str: str}:
    return {
        'object': str(model)
    }


def output_formatted_data_from_dict(format_value: MyEnum, info_list: list[any] | dict) -> Response:
    if format_value == MyEnum.XML:
        resp = dict2xml(info_list, indent=" ")
        return Response(response=resp, status=200, headers={'Content-Type': 'application/xml'})
    else:
        json_str = json.dumps(info_list)
        return Response(response=json_str.encode('utf-8'), status=200, headers={'Content-Type': 'application/json'})


def output_formatted_data_from_list(format_value: MyEnum, info_list: list[any] | dict,
                                    element_name: str = 'element') -> Response:
    if format_value == MyEnum.XML:
        elements = ET.Element("response")

        for item_info in info_list:
            element = ET.SubElement(elements, element_name)
            if isinstance(item_info, dict):
                for key, value in item_info.items():
                    ET.SubElement(element, key).text = str(value)
            else:
                ET.SubElement(element, "value").text = str(item_info)

        resp = ET.tostring(elements, encoding="unicode")

        return Response(response=resp, status=200, headers={'Content-Type': 'application/xml'})
    else:
        json_list = [serialize_model(model) for model in info_list]
        json_str = json.dumps(json_list)
        return Response(response=json_str.encode('utf-8'), status=200, headers={'Content-Type': 'application/json'})


class Students(Resource):

    @swag_from('swagger/Student.yml')
    def get(self):
        response_format = MyEnum(request.args.get('format', default='json'))
        student_query = session.query(StudentModel)

        if request.args.get('student_id'):
            student_id = request.args.get('student_id')
            student = student_query.filter_by(id=student_id).first()
            response = serialize_model(student)
            return output_formatted_data_from_dict(response_format, response)

        elif request.args.get('first_name'):
            first_name = request.args.get('first_name').capitalize()
            student = student_query.filter_by(first_name=first_name).all()
            response = [serialize_model(student) for student in student]
            return output_formatted_data_from_dict(response_format, response)

        elif request.args.get('last_name'):
            last_name = request.args.get('last_name').capitalize()
            student = student_query.filter_by(last_name=last_name).all()
            response = [serialize_model(student) for student in student]
            return output_formatted_data_from_dict(response_format, response)

        elif request.args.get('course_name'):
            course_name = request.args.get('course_name').capitalize()
            course = session.query(CourseModel).filter_by(name=course_name).first()
            if not course:
                return output_formatted_data_from_dict(response_format, {'error': 'Course not found'})

            students_on_course = course.students
            response = [serialize_model(student) for student in students_on_course]
            return output_formatted_data_from_list(response_format, response)

        else:
            students = session.query(StudentModel)
            response = [serialize_model(student) for student in students]

            return output_formatted_data_from_list(response_format, response)

    @swag_from('swagger/CreateStudent.yml')
    def post(self) -> Response:
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        group_id = request.args.get('group_id')
        response_format = MyEnum(request.args.get('format', default='json'))
        response = create_new_student(first_name, last_name, group_id)
        return output_formatted_data_from_dict(response_format, response)

    @swag_from('swagger/DeleteStudent.yml')
    def delete(self) -> Response:
        student_id = request.args.get('student_id')
        response_format = MyEnum(request.args.get('format', default='json'))
        response = delete_student(int(student_id))
        return output_formatted_data_from_dict(response_format, response)


class Groups(Resource):
    @swag_from('swagger/FindGroupsWithStudentCount.yml')
    def get(self) -> Response:
        stud_count = request.args.get('student_count', default=20)
        response_format = MyEnum(request.args.get('format', default='json'))
        groups = find_groups_with_student_count(stud_count)
        response = serialize_model(groups)
        return output_formatted_data_from_dict(response_format, response)


class Courses(Resource):
    @swag_from('swagger/AddStudentToTheCourse.yml')
    def patch(self):
        response_format = MyEnum(request.args.get('format', default='json'))
        student_id = request.args.get('student_id')
        course_id = request.args.get('course_id')
        response = add_student_to_the_course(int(student_id), int(course_id))
        return output_formatted_data_from_dict(response_format, response)

    @swag_from('swagger/RemoveStudentFromCourse.yml')
    def delete(self) -> Response:
        response_format = MyEnum(request.args.get('format', default='json'))
        student_id = request.args.get('student_id')
        course_id = request.args.get('course_id')
        response = remove_student_from_course(int(student_id), int(course_id))
        return output_formatted_data_from_dict(response_format, response)
