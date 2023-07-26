from flasgger import Swagger
from flask import Flask
from flask_restful import Api

from web_app.api import (AddStudentToTheCourse, CreateStudent, DeleteStudent,
                         FindGroupsWithStudentCount,
                         FindStudentsRelatedToTheCourse, HelloWorld,
                         RemoveStudentFromCourse)

app = Flask(__name__)
api = Api(app)

api.add_resource(HelloWorld, '/')
api.add_resource(FindGroupsWithStudentCount, '/api/v1/groups', methods=['GET'])
api.add_resource(FindStudentsRelatedToTheCourse, '/api/v1/students/courses', methods=['GET'])
api.add_resource(CreateStudent, '/api/v1/students', methods=['POST'])
api.add_resource(DeleteStudent, '/api/v1/students/<student_id>', methods=['DELETE'])
api.add_resource(AddStudentToTheCourse, '/api/v1/students/<student_id>/courses/<course_id>', methods=['PATCH'])
api.add_resource(RemoveStudentFromCourse, '/api/v1/student/<student_id>/courses/<course_id>', methods=['DELETE'])

swagger = Swagger(app)

if __name__ == '__main__':
    pass
