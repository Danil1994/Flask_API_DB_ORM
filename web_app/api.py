from __future__ import annotations

import json
import xml.etree.ElementTree as ET

from dict2xml import dict2xml
from flasgger import swag_from
from flask import Response, request
from flask_restful import Resource

from web_app.constants import MyEnum
from web_app.db.orm_commands import (add_student_to_the_course,
                                     create_new_student, delete_student,
                                     find_groups_with_student_count,
                                     find_students_related_to_the_course,
                                     remove_student_from_course)


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
        print(json_list)
        json_str = json.dumps(json_list)
        return Response(response=json_str.encode('utf-8'), status=200, headers={'Content-Type': 'application/json'})


class FindGroupsWithStudentCount(Resource):
    @swag_from('swagger/FindGroupsWithStudentCount.yml')
    def get(self) -> Response:
        stud_count = request.args.get('student_count', default=20)
        response_format = MyEnum(request.args.get('format', default='json'))
        response = find_groups_with_student_count(stud_count)

        return output_formatted_data_from_list(response_format, response)


class FindStudentsRelatedToTheCourse(Resource):
    @swag_from('swagger/FindStudentsRelatedToTheCourse.yml')
    def get(self) -> Response:
        course_name = request.args.get('course')
        response_format = MyEnum(request.args.get('format', default='json'))
        response = find_students_related_to_the_course(course_name)

        return output_formatted_data_from_list(response_format, response)


class CreateStudent(Resource):
    @swag_from('swagger/CreateStudent.yml')
    def post(self) -> Response:
        first_name = request.args.get('first_name')
        last_name = request.args.get('last_name')
        response_format = MyEnum(request.args.get('format', default='json'))
        response = create_new_student(first_name, last_name)
        return output_formatted_data_from_dict(response_format, response)


class DeleteStudent(Resource):
    @swag_from('swagger/DeleteStudent.yml')
    def delete(self, student_id) -> Response:
        response_format = MyEnum(request.args.get('format', default='json'))
        response = delete_student(student_id)
        return output_formatted_data_from_dict(response_format, response)


class AddStudentToTheCourse(Resource):
    @swag_from('swagger/AddStudentToTheCourse.yml')
    def get(self, student_id, course_id) -> Response:
        response_format = MyEnum(request.args.get('format', default='json'))
        response = add_student_to_the_course(student_id, course_id)
        return output_formatted_data_from_dict(response_format, response)


class RemoveStudentFromCourse(Resource):
    @swag_from('swagger/RemoveStudentFromCourse.yml')
    def patch(self, student_id, course_id) -> Response:
        response_format = MyEnum(request.args.get('format', default='json'))
        response = remove_student_from_course(student_id, course_id)
        return output_formatted_data_from_dict(response_format, response)


class HelloWorld(Resource):
    def get(self):
        return {
            'hello': "Its hello page, you may use next url : '/api/v1/groups',  '/api/v1/students',   /"
                     "'/api/v1/student/add', '/api/v1/student/del/<student_id>', /"
                     "'/api/v1/student/<student_id>/add_course/<course_id>', /"
                     "'/api/v1/student/<student_id>/course/<course_id>"}
