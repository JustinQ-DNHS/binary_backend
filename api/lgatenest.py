from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from __init__ import db
from model.nestPost import NestPost
from api.jwt_authorize import token_required

lgate_api = Blueprint('lgate_api', __name__, url_prefix='/api')
api = Api(lgate_api)

class NestPostCRUD(Resource):
    @token_required
    def post(self):
        data = request.get_json()

        if 'name' not in data or 'score' not in data:
            return jsonify({"error": "Missing 'name' or 'score'"}), 400

        try:
            new_post = NestPost(
                user_id=g.current_user.id,
                name=data['name'],
                score=data['score']
            )

            new_post.create()

            return jsonify(new_post.read()), 201

        except Exception as e:
            print(f"Error creating post: {e}")
            return jsonify({"error": str(e)}), 500

    @token_required
    def get(self):
        try:
            results = NestPost.query.all()
            data = [result.read() for result in results]
            return jsonify(data), 200
        except Exception as e:
            print(f"Error fetching data: {e}")
            return jsonify({"error": str(e)}), 500

api.add_resource(NestPostCRUD, '/lgate')