from flask import Blueprint
from flask_restful import Api, Resource # used for REST API building

student_api = Blueprint('student_api', __name__,
                   url_prefix='/api')

# API docs https://flask-restful.readthedocs.io/en/latest/
api = Api(student_api)

class StudentAPI:        
    class _Manahil(Resource): 
        def get(self):
           # implement the get method 
           pass
    
    class _Justin(Resource): 
        def get(self):
           # implement the get method 
           pass

    class _Vincent(Resource): 
        def get(self):
           # implement the get method 
           pass
        
    class _Shriya(Resource): 
        def get(self):
           # implement the get method 
           pass

    class _Lars(Resource): 
        def get(self):
           # implement the get method 
           pass

    class _Weston(Resource): 
        def get(self):
           # implement the get method 
           pass
    
    class _Shaurya(Resource): 
        def get(self):
           # implement the get method 
           pass
    
    class _Rutvik(Resource): 
        def get(self):
           # implement the get method 
           pass

    class _Students(Resource): 
        def get(self):
           # implement the get method 
           pass

    # building RESTapi endpoint
    api.add_resource(_Manahil, '/student/manahil')          
    api.add_resource(_Justin, '/student/justin')
    api.add_resource(_Vincent, '/student/vincent')
    api.add_resource(_Shriya, '/student/shriya')
    api.add_resource(_Lars, '/student/lars')
    api.add_resource(_Weston, '/student/weston')
    api.add_resource(_Shaurya, '/student/shaurya')
    api.add_resource(_Rutvik, '/student/rutvik')
    api.add_resource(_Students, '/students')