import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.feedback import Feedback

"""
This Blueprint object is used to define APIs for the Feedback model.
- Blueprint is used to modularize application files.
- This Blueprint is registered to the Flask app in main.py.
"""
feedback_api = Blueprint('feedback_api', __name__, url_prefix='/api')

"""
The Api object is connected to the Blueprint object to define the API endpoints.
- The API object is used to add resources to the API.
- The objects added are mapped to code that contains the actions for the API.
- For more information, refer to the API docs: https://flask-restful.readthedocs.io/en/latest/api.html
"""
api = Api(feedback_api)

class FeedbackAPI:
    """
    Define the API CRUD endpoints for the Feedback model.
    There are four operations that correspond to common HTTP methods:
    - feedback: create a new feedback
    - get: read feedbacks
    - put: update a feedback
    - delete: delete a feedback
    """
    class _CRUD(Resource):
        @token_required()
        def post(self):
            # Obtain the current user from the token required setting in the global context
            current_user = g.current_user
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Create a new feedback object using the data from the request
            feedback = feedback(data['content'], data['post_id'], current_user.id)
            # Save the feedback object using the Object Relational Mapper (ORM) method defined in the model
            feedback.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(feedback.read())

        @token_required()
        def get(self):
            # Obtain the id of the post
            data = request.get_json()
            post_id = data['id']
            # Find all the feedbacks by the current user
            feedbacks = Feedback.query.filter(Feedback._post_id == data['id']).all()
            # Prepare a JSON list of all the feedbacks, uses for loop shortcut called list comprehension
            json_ready = [feedback.read() for feedback in feedbacks]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)

        @token_required()
        def put(self):
            # Obtain the current user
            current_user = g.current_user
            # Obtain the request data
            data = request.get_json()
            # Find the current feedback from the database table(s)
            feedback = Feedback.query.get(data['id'])
            # Update the feedback
            feedback._content = data['content']
            # Save the feedback
            feedback.update()
            # Return response
            return jsonify(feedback.read())

        @token_required()
        def delete(self):
            # Obtain the current user
            current_user = g.current_user
            # Obtain the request data
            data = request.get_json()
            # Find the current feedback from the database table(s)
            feedback = Feedback.query.get(data['id'])
            # Delete the feedback using the ORM method defined in the model
            feedback.delete()
            # Return response
            return jsonify({"message": "Feedback deleted"})

    """
    Map the _CRUD class to the API endpoints for /feedback.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    """
    api.add_resource(_CRUD, '/feedback')