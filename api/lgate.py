import jwt
from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from __init__ import app

CORS(app)
lgate_api = Blueprint('lgate_api', __name__, url_prefix='/api')
api = Api(lgate_api)

class GroupAPI:
    class _CRUD(Resource):
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