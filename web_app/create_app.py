from flasgger import Swagger
from flask import Flask
from flask_restful import Api

from web_app.api import Courses, Groups, Students

app = Flask(__name__)
api = Api(app)

api.add_resource(Students, '/api/v1/students/', methods=['POST', 'GET', 'DELETE'])
api.add_resource(Courses, '/api/v1/students/courses/', methods=['PATCH', 'DELETE'])
api.add_resource(Groups, '/api/v1/groups')


swagger = Swagger(app)

if __name__ == '__main__':
    pass
