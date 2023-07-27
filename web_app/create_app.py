from flasgger import Swagger
from flask import Flask
from flask_restful import Api, reqparse, Resource
from flasgger import swag_from
# from flask_restplus import Namespace


from web_app.api import (AddStudentToTheCourse, CreateStudent, DeleteStudent,
                         FindGroupsWithStudentCount,
                         FindStudentsRelatedToTheCourse, HelloWorld,
                         RemoveStudentFromCourse,
                         )

app = Flask(__name__)
api = Api(app)

# ns = Namespace('students', description='Student operations')


student_parser = reqparse.RequestParser()
student_parser.add_argument('first_name', type=str, location='args')
student_parser.add_argument('last_name', type=str, location='args')
student_parser.add_argument('course', type=str)
student_parser.add_argument('group_id', type=int)
student_parser.add_argument('format', type=str, default='json')


class Students(Resource):
    def __init__(self, student_parser):
        self.student_parser = student_parser

    @swag_from('swagger/CreateStudent.yml')
    def get(self):
        args = self.student_parser
        return (args['first_name'])


api.add_resource(Students, '/api/v1/students/', methods=['POST', 'GET', 'PATCH'])

# api.add_resource(HelloWorld, '/')
# api.add_resource(FindGroupsWithStudentCount, '/api/v1/groups', methods=['GET'])
# api.add_resource(FindStudentsRelatedToTheCourse, '/api/v1/students/courses', methods=['GET'])
# api.add_resource(AddStudentToTheCourse, '/api/v1/students/<student_id>/courses/<course_id>', methods=['PATCH'])
#
#
# api.add_resource(DeleteStudent, '/api/v1/students/<student_id>', methods=['DELETE'])
# api.add_resource(RemoveStudentFromCourse, '/api/v1/student/<student_id>/courses/<course_id>', methods=['DELETE'])

swagger = Swagger(app)

if __name__ == '__main__':
    pass
