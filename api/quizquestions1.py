from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from api.jwt_authorize import token_required
# from model.quizquestions import quizquestions
from model.nestPost import NestPost

quizquestions_api = Blueprint('quizquestions_api', __name__, url_prefix='/api')

"""
The Api object is connected to the Blueprint object to define the API endpoints.
- The API object is used to add resources to the API.
- The objects added are mapped to code that contains the actions for the API.
- For more information, refer to the API docs: https://flask-restful.readthedocs.io/en/latest/api.html
"""
api = Api(quizquestions_api)

class quizquestionsAPI:
    """
    Define the API CRUD endpoints for the Post model.
    There are four operations that correspond to common HTTP methods:
    - post: create a new post
    - get: read posts
    - put: update a post
    - delete: delete a post
    """
    class _CRUD(Resource):
        @token_required()
        def get(self):
            # Find all the posts by the current user
            # scores = quizquestions.query.all()
            scores = NestPost.query.all()
            # Prepare a JSON list of all the posts, uses for loop shortcut called list comprehension
            json_ready = [score.read() for score in scores]
            # Return a JSON list, converting Python dictionaries to JSON format
            #return jsonify(json_ready)
            return jsonify("Shriya is so cool")


    """
    Map the _CRUD class to the API endpoints for /post.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    """
    api.add_resource(_CRUD, '/quizquestions/guizquestions')