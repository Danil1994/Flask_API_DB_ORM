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
api.add_resource(FindGroupsWithStudentCount, '/api/v1/groups')
api.add_resource(FindStudentsRelatedToTheCourse, '/api/v1/students')
api.add_resource(CreateStudent, '/api/v1/students')
api.add_resource(DeleteStudent, '/api/v1/students/<student_id>')
api.add_resource(AddStudentToTheCourse, '/api/v1/students/<student_id>/courses/<course_id>')
api.add_resource(RemoveStudentFromCourse, '/api/v1/student/<student_id>/courses/<course_id>')

swagger = Swagger(app)

if __name__ == '__main__':
    pass
