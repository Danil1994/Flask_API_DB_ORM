from flasgger import Swagger
from flask import Flask
from flask_restful import Api


from web_app.api import (AddStudentToTheCourse,
                         DeleteStudent,
                         FindGroupsWithStudentCount,
                         FindStudentsRelatedToTheCourse,
                         HelloWorld,
                         CreateStudent, RemoveStudentFromCourse)

app = Flask(__name__)
api = Api(app)

api.add_resource(HelloWorld, '/')
api.add_resource(FindGroupsWithStudentCount, '/api/v1/groups')
api.add_resource(FindStudentsRelatedToTheCourse, '/api/v1/students')
api.add_resource(CreateStudent, '/api/v1/student/create')
api.add_resource(DeleteStudent, '/api/v1/student/del/<student_id>')
api.add_resource(AddStudentToTheCourse, '/api/v1/student/<student_id>/add_course/<course_id>')
api.add_resource(RemoveStudentFromCourse, '/api/v1/student/<student_id>/remove_course/<course_id>')

swagger = Swagger(app)

if __name__ == '__main__':
    pass
