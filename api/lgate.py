import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.nestPost import NestPost

"""
This Blueprint object is used to define APIs for the Post model.
- Blueprint is used to modularize application files.
- This Blueprint is registered to the Flask app in main.py.
"""
lgate_api = Blueprint('lgate_api', __name__, url_prefix='/api')

"""
The Api object is connected to the Blueprint object to define the API endpoints.
- The API object is used to add resources to the API.
- The objects added are mapped to code that contains the actions for the API.
- For more information, refer to the API docs: https://flask-restful.readthedocs.io/en/latest/api.html
"""
api = Api(lgate_api)

class GroupAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Save quiz results from the frontend to the database.
            """
            current_user = g.current_user
            data = request.get_json() 

            if 'name' not in data or 'score' not in data:
                return jsonify({"error": "Missing required fields: 'name' and 'score'"}), 400
            
            lgquiz = lgate(
                user_id=current_user.id,
                name=data['name'],
                score=data['score']
            )

            try:
                lgquiz.create()
                return jsonify(lgquiz.read()), 201
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        def get(self):
            """
            Retrieve all quiz results for the authenticated user.
            """
            current_user = g.current_user
            results = lgate.query.filter_by(user_id=current_user.id).all()
            return jsonify([result.read() for result in results])

    """
    Map the _CRUD class to the API endpoints for /post.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    """
    api.add_resource(_CRUD, '/lgate')