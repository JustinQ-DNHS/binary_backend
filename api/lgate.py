import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource 
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.nestPost import NestPost  

lgate_api = Blueprint('lgate_api', __name__, url_prefix='/api')


api = Api(lgate_api)

class GroupAPI:
    """
    Define the API CRUD endpoints for the Group model (e.g., lgate quiz results).
    There are two operations defined here: 
    - post: to save the quiz results
    - get: to retrieve quiz results for the authenticated user
    """

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

            lgquiz = NestPost(
                user_id=current_user.id,
                name=data['name'],
                score=data['score']
            )

            try:
                lgquiz.create() 
                return jsonify(lgquiz.read()), 201 
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @token_required()  
        def get(self):
            """
            Retrieve all quiz results for the authenticated user.
            """
            current_user = g.current_user
            results = NestPost.query.filter_by(user_id=current_user.id).all() 

            return jsonify([result.read() for result in results])

    api.add_resource(_CRUD, '/lgate')
