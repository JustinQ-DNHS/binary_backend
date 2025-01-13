import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource
from __init__ import app, db
from api.jwt_authorize import token_required
from model.nestPost import NestPost

lgate_api = Blueprint('lgate_api', __name__, url_prefix='/api')
api = Api(lgate_api)

class GroupAPI:
    class _CRUD(Resource):
        @token_required
        def post(self):
            """
            Save Logic Gates Quiz results: name, score, and user_id.
            """
            current_user = g.current_user
            data = request.get_json()

            if 'name' not in data or 'score' not in data:
                return jsonify({"error": "Missing required fields: 'name' and 'score'"}), 400

            #  Create a new set for Logic Gates Game
            lgquiz = NestPost(
                user_id=current_user.id,
                name=data['name'],
                score=data['score']
            )

            try:
                lgquiz.create()

                #  Return the given data
                response_data = {
                    "id": lgquiz.id,
                    "user_id": lgquiz.user_id,
                    "name": lgquiz.name,
                    "score": lgquiz.score
                }

                return jsonify(response_data), 201
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @token_required
        def get(self):
            """
            Retrieve all Logic Gates Quiz results.
            """
            try:
                results = NestPost.query.all()
                data = [
                    {
                        "id": result.id,
                        "user_id": result.user_id,
                        "name": result.name,
                        "score": result.score
                    }
                    for result in results
                ]
                return jsonify(data), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

api.add_resource(GroupAPI._CRUD, '/lgate')