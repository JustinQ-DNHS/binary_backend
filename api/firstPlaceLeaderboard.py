from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource  # used for REST API building
from api.jwt_authorize import token_required
from model.firstPlaceLeaderboard import firstPlaceLeaderboard

"""
This Blueprint object is used to define APIs for the Post model.
- Blueprint is used to modularize application files.
- This Blueprint is registered to the Flask app in main.py.
"""
firstPlaceLeaderboard_api = Blueprint('firstPlaceLeaderboard_api', __name__, url_prefix='/api')

"""
The Api object is connected to the Blueprint object to define the API endpoints.
- The API object is used to add resources to the API.
- The objects added are mapped to code that contains the actions for the API.
- For more information, refer to the API docs: https://flask-restful.readthedocs.io/en/latest/api.html
"""
api = Api(firstPlaceLeaderboard_api)

class FirstPlaceLeaderboardAPI:
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
        def post(self):
            # Obtain the current user from the token
            current_user = g.current_user
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Create a new post object using the data from the request
            time = firstPlaceLeaderboard(data['username'], current_user.id, data['score'], data['difficulty'])
            # Save the post object using the ORM method defined in the model
            time.create()
            # Return response to the client in JSON format
            return jsonify(time.read())

        def get(self):
            # Obtain the current user
            # current_user = g.current_user
            # Find all the posts by the current user
            times = firstPlaceLeaderboard.query.all()
            # Prepare a JSON list of all the posts, uses for loop shortcut called list comprehension
            json_ready = [time.read() for time in times]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)

        @token_required()
        def delete(self):
            # Obtain the current user
            current_user = g.current_user
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            time = firstPlaceLeaderboard.query.get(data['id'])
            # Delete the post using the ORM method defined in the model
            time.delete()
            # Return response
            return jsonify({"message": "Post deleted"})

    """
    Map the _CRUD class to the API endpoints for /post.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    """
    api.add_resource(_CRUD, '/firstPlaceLeaderboard')