from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource
from __init__ import app, db
from model.newQuizCreation import QuizCreation  # Make sure this imports the correct model

# Blueprint setup for the API
quiz_api = Blueprint('quiz_api', __name__, url_prefix='/api')

# API object setup
api = Api(quiz_api)

class QuizAPI:
    """
    Define API endpoints for QuizCreation model.
    """
    class _CRUD(Resource):
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

        def get(self):
            """
            Retrieve all quizzes.
            """
            quizzes = QuizCreation.query.all()
            return jsonify([quiz.read() for quiz in quizzes])

        def put(self):
            """
            Update an existing quiz by its ID.
            """
            data = request.get_json()
            if 'id' not in data or 'question' not in data or 'answer' not in data:
                return {'message': 'ID, question, and answer are required'}, 400

            quiz = QuizCreation.query.get(data['id'])
            if not quiz:
                return {'message': 'Quiz not found'}, 404

            try:
                # Update quiz
                quiz._question = data['question']
                quiz._answer = data['answer']
                db.session.commit()
                return jsonify({'message': 'Quiz updated', 'quiz': quiz.read()})

            except Exception as e:
                db.session.rollback()
                return {'message': f'Error updating quiz: {str(e)}'}, 500

        def delete(self):
            """
            Delete a quiz by its ID.
            """
            data = request.get_json()
            if 'id' not in data:
                return {'message': 'ID is required'}, 400

            quiz = QuizCreation.query.get(data['id'])
            if not quiz:
                return {'message': 'Quiz not found'}, 404

            try:
                quiz.delete()
                return jsonify({'message': 'Quiz deleted'})

            except Exception as e:
                db.session.rollback()
                return {'message': f'Error deleting quiz: {str(e)}'}, 500

    # Add resource endpoints to API
    api.add_resource(_CRUD, '/quiz', '/quiz/<int:id>')  # Routes for single quiz creation, update, get, and delete

# Register the blueprint with the app
app.register_blueprint(quiz_api)
