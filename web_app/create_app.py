
from flask import Flask
from flask_restful import Api

from web_app.api import (AddStudentToTheCourse, DeleteStudent,
                         FindGroupsWithStudentCount,
                         FindStudentsRelatedToTheCourse, HelloWorld,
                         NewStudent, RemoveStudentFromCourse)


app = Flask(__name__)
api = Api(app)

api.add_resource(HelloWorld, '/')
api.add_resource(FindGroupsWithStudentCount, '/api/v1/groups')
api.add_resource(FindStudentsRelatedToTheCourse, '/api/v1/students')
api.add_resource(NewStudent, '/api/v1/student/add')
api.add_resource(DeleteStudent, '/api/v1/student/del/<student_id>')
api.add_resource(AddStudentToTheCourse, '/api/v1/student/<student_id>/add_course/<course_id>')
api.add_resource(RemoveStudentFromCourse, '/api/v1/student/<student_id>/course/<course_id>')

if __name__ == '__main__':
    app.run(debug=True)
