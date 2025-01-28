from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from __init__ import app
from api.jwt_authorize import token_required
from model.newQuizCreation import QuizCreation

# Blueprint setup for the API
quizCreation_api = Blueprint('quizCreation_api', __name__, url_prefix='/api')

api = Api(quizCreation_api)

class QuizCreationAPI:
    """
    Define API endpoints for QuizCreation model.
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
            if 'question' not in data or 'answer' not in data or 'quiz_id' not in data:
                return {'message': 'Question, answer, and quiz_id are required'}, 400

            try:
                # Create new quiz
                quiz = QuizCreation(
                    question=data['question'],
                    answer=data['answer'],
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
            # quizzes = QuizCreation.query.all()
            # json_ready = [quiz.read() for quiz in quizzes]
            return jsonify("I'm a stupid ass quizzes")

        @token_required
        def put(self):
            """
            Update an existing quiz by its ID.
            """
            data = request.get_json()
            if 'id' not in data or 'question' not in data or 'answer' not in data:
                return {'message': 'ID, question, and answer are required'}, 400

            quiz = QuizCreation.query.get(data['id']).update()
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

            quiz = QuizCreation.query.get(data['id']).delete()
            # if not quiz:
            #     return {'message': 'Quiz not found'}, 404

            # try:
            #     quiz.delete()
            #     return jsonify({'message': 'Quiz deleted'})

            # except Exception as e:
            #     db.session.rollback()
            #     return {'message': f'Error deleting quiz: {str(e)}'}, 500

    # Add resource endpoints to API
    api.add_resource(_CRUD, '/quiz')  # Routes for single quiz creation, update, get, and delete

# Register the blueprint with the app
#app.register_blueprint(quizCreation_api)
