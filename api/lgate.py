import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource
from datetime import datetime
from __init__ import app, db  # ✅ FIX: Imported db here
from api.jwt_authorize import token_required
from model.nestPost import NestPost  

lgate_api = Blueprint('lgate_api', __name__, url_prefix='/api')
api = Api(lgate_api)

class GroupAPI:
    """
    Define the API CRUD endpoints for the Group model (e.g., lgate quiz results).
    """

    class _CRUD(Resource):
        @token_required
        def post(self):
            """
            Save quiz results from the frontend.
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

        @token_required
        def get(self):
            """
            Retrieve all quiz results for the authenticated user.
            """
            try:
                # Fetch ALL quiz results
                results = NestPost.query.all()

                # Debug: Print raw query results
                print("Fetched Results:", results)

                # Serialize results
                data = [result.read() for result in results]
                print("Serialized Data:", data)

                return jsonify(data), 200
            except Exception as e:
                print(f"Error in GET /api/lgate: {e}")
                return jsonify({"error": str(e)}), 500

# ✅ FIX: Now db is properly imported
@lgate_api.route('/lgate/test-data', methods=['POST'])
def add_test_data():
    try:
        # Create sample quiz data
        test_data = [
            NestPost(user_id=101, name="AND Gate Quiz", score=5),
            NestPost(user_id=102, name="OR Gate Quiz", score=3),
            NestPost(user_id=103, name="XOR Gate Quiz", score=4)
        ]

        # Add and commit data to the database
        for item in test_data:
            db.session.add(item)
        db.session.commit()

        return jsonify({"message": "Test data added successfully"}), 201
    except Exception as e:
        print(f"Error adding test data: {e}")
        return jsonify({"error": str(e)}), 500

# Ensure the resource is registered
api.add_resource(GroupAPI._CRUD, '/lgate')