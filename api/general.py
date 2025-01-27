# # This is a file that will be used to contain API's and and HTTP that require access to multiple parts of our backend

# from flask import Blueprint, request, jsonify, current_app, Response, g
# from flask_restful import Api, Resource  # used for REST API building
# from datetime import datetime
# from __init__ import app
# from api.jwt_authorize import token_required
# from model.binaryLearningGame import binaryLearningGameScores

# general_api = Blueprint('general_api', __name__, url_prefix='/api')

# """
# The Api object is connected to the Blueprint object to define the API endpoints.
# - The API object is used to add resources to the API.
# - The objects added are mapped to code that contains the actions for the API.
# - For more information, refer to the API docs: https://flask-restful.readthedocs.io/en/latest/api.html
# """
# api = Api(general_api)

# class GeneralAPI:
#     """
#     Define the API CRUD endpoints for the Post model.
#     There are four operations that correspond to common HTTP methods:
#     - post: create a new post
#     - get: read posts
#     - put: update a post
#     - delete: delete a post
#     """
#     class _CRUD(Resource):
#         @token_required()
#         def get(self):
#             # Find all the posts by the current user
#             scores = binaryLearningGameScores.query.all()
#             # Prepare a JSON list of all the posts, uses for loop shortcut called list comprehension
#             json_ready = [score.read() for score in scores]
#             # Return a JSON list, converting Python dictionaries to JSON format
#             return jsonify(json_ready)


#     """
#     Map the _CRUD class to the API endpoints for /post.
#     - The API resource class inherits from flask_restful.Resource.
#     - The _CRUD class defines the HTTP methods for the API.
#     """
#     api.add_resource(_CRUD, '/general/binaryScores')