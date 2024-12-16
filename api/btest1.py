import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.btest1 import btest1
from model.user import User
from model.section import Section

# """
# This Blueprint object is used to define APIs for the Group model.
# - Blueprint is used to modularize application files.
# - This Blueprint is registered to the Flask app in main.py.
# """
# group_api = Blueprint('group_api', __name__, url_prefix='/api')
btest1_api = Blueprint('btest1_api', __name__, url_prefix='/api')

# """
# The Api object is connected to the Blueprint object to define the API endpoints.
# - The API object is used to add resources to the API.
# - The objects added are mapped to code that contains the actions for the API.
# - For more information, refer to the API docs: https://flask-restful.readthedocs.io/en/latest/api.html
# """
# api = Api(group_api)
api = Api(btest1_api)

class GroupAPI:
    """
    Define the API CRUD endpoints for the Group model.
    There are four operations that correspond to common HTTP methods:
    - post: create a new group
    - get: read groups
    - put: update a group
    - delete: delete a group
    """
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new group.
            """
            print(request.get_json())
            # Obtain the current user from the token required setting in the global context
            current_user = g.current_user
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            print(data)
            # Create a new group object using the data from the request
            chat = btest1(data['message'], current_user.id)
            # Save the chat object using the Object Relational Mapper (ORM) method defined in the model
            chat.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(chat.read())
        def get(self):
            chats = btest1.query.all()
            allChats = []
            for i in range(len(chats)):
                allChats.append(chats[i].read())

            # Return a JSON restful response to the client
            return jsonify(allChats)
        
    api.add_resource(_CRUD, '/car_chat')