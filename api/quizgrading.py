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

        def post(self):
            """
            Create a new group.
            """
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Create a new group object using the data from the request
            chat = quizgrading(data['quizgrade'], data['attempt'])
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

        def put(self):
            # Obtain the current user
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            post = quizgrading.query.get(data['id'])
            # Update the post
            post._quizgrade = data['quizgrade']
            post._attempt = data['attempt']
            # Save the post
            post.update()
            # Return response
            return jsonify(post.read())

        def delete(self):
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            post = quizgrading.query.get(data['id'])
            # Delete the post using the ORM method defined in the model
            post.delete()
            # Return response
            return jsonify({"message": "Post deleted"})

    """
    Map the _CRUD class to the API endpoints for /post.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    """
        
    api.add_resource(_CRUD, '/quizgrading')
    
if __name__ == '__main__':
    app.run(debug=True)