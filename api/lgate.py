from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from __init__ import app
from api.jwt_authorize import token_required
from model.lgatedata import lgate

# Blueprint setup for the API
lgate_api = Blueprint('lgate_api', __name__, url_prefix='/api/lgate')

api = Api(lgate_api)

# test data

@lgate_api.route('/test', methods=['GET'])
def test_lgate():
    return {"message": "Logic Gate API is working!"}

lgate = [
    { "name": "", "score": "3", "quiz_id": "1"},
]
class lgateAPI:
    """
    Define API endpoints for lgate model.
    """
    class _CRUD(Resource):
        @token_required
        def post(self):
            """
            Create a new quiz.
            """
            # Get data from request
            data = request.get_json()

            # Validate required fields
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'name' not in data or 'score' not in data or 'quiz_id' not in data:
                return {'message': 'name, score, and quiz_id are required'}, 400

            try:
                # Create new quiz
                quiz = lgate(
                    name=data['name'],
                    score=data['score'],
                    quiz_id=data['quiz_id']
                )
                quiz.create()  # Using the create method defined in your model
                return jsonify({'message': 'Quiz created', 'quiz': quiz.read()}), 201

            except Exception as e:
                return {'message': f'Error creating quiz: {str(e)}'}, 500

        @token_required
        def get(self):
            """
            Retrieve all quizzes.
            """
            quizzes = lgate.query.all()
            return jsonify([quiz.read() for quiz in quizzes])

        @token_required
        def put(self):
            """
            Update an existing quiz by its ID.
            """
            data = request.get_json()
            if 'id' not in data or 'name' not in data or 'score' not in data:
                return {'message': 'ID, name, and score are required'}, 400

            quiz = lgate.query.get(data['id']).update()
            if not quiz:
                return {'message': 'Quiz not found'}, 404


        @token_required
        def delete(self):
            """
            Delete a quiz by its ID.
            """
            data = request.get_json()
            if 'id' not in data:
                return {'message': 'ID is required'}, 400

            quiz = lgate.query.get(data['id']).delete()
            # if not quiz:
            #     return {'message': 'Quiz not found'}, 404

            # try:
            #     quiz.delete()
            #     return jsonify({'message': 'Quiz deleted'})

            # except Exception as e:
            #     db.session.rollback()
            #     return {'message': f'Error deleting quiz: {str(e)}'}, 500

@lgate_api.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Logic Gate API Root is working!"})

    # Add resource endpoints to API
    api.add_resource(_CRUD, 'lgate')  # Routes for single quiz creation, update, get, and delete

# Register the blueprint with the app
#app.register_blueprint(lgate_api)
