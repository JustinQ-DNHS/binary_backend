import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from flask_cors import CORS
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.quizgrading import quizgrading
from model.user import User
from model.section import Section

quizgrading_api = Blueprint('quizgrading_api', __name__, url_prefix='/api')

CORS(app)

api = Api(quizgrading_api)

class GroupAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Save quiz results from the frontend to the database.
            """
            current_user = g.current_user  # Get authenticated user
            data = request.get_json()  # Get quiz data from the request

            # Validate incoming data
            if 'score' not in data or 'attempt_number' not in data:
                return jsonify({"error": "Missing required fields: 'score' and 'attempt_number'"}), 400

            # Create a new quiz grading entry
            quiz_result = quizgrading(
                user_id=current_user.id,
                score=data['score'],
                attempt_number=data['attempt_number']
            )

            try:
                quiz_result.create()  # Save to the database
                return jsonify(quiz_result.read()), 201
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        def get(self):
            """
            Retrieve all quiz results for the authenticated user.
            """
            current_user = g.current_user
            results = quizgrading.query.filter_by(user_id=current_user.id).all()
            return jsonify([result.read() for result in results])
        
    api.add_resource(_CRUD, '/quizgrading')