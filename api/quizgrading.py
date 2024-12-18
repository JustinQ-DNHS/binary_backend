import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.quizgrading import quizgrading
from model.user import User
from model.section import Section

quizgrading_api = Blueprint('quizgrading_api', __name__, url_prefix='/api')

api = Api(quizgrading_api)

class GroupAPI:
    """
    The API CRUD endpoints correspond to common HTTP methods:
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
            # Obtain the current user from the token required setting in the global context
            current_user = g.current_user
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Create a new group object using the data from the request
            chat = quizgrading(data['message'], current_user.id)
            # Save the chat object using the Object Relational Mapper (ORM) method defined in the model
            chat.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(chat.read())
        
        def get(self):
            chats = quizgrading.query.all()
            allChats = []
            for i in range(len(chats)):
                allChats.append(chats[i].read())

            # Return a JSON restful response to the client
            return jsonify(allChats)
        
    api.add_resource(_CRUD, '/quizgrading')