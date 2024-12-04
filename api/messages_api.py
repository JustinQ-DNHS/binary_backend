# by P5 G1
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import requests
import json

# Create a Blueprint for the messages API
messages_api = Blueprint('messages_api', __name__, url_prefix='/api')
api = Api(messages_api)

# Path for the messages file
MESSAGE_FILE_PATH = 'Period-5/aaak/messages.txt'

# API Key and URL template for the trivia API
API_KEY = 'LUDk78PjUOELr1cvaaQuEA==t3yAhXp37UD4j6P9'
TRIVIA_API_URL = 'https://api.api-ninjas.com/v1/trivia?category={}'

class MessagesAPI:
    # Define the API CRUD endpoints for the messages file.
    
    class _Messages(Resource):
        def get(self):
            """Retrieve all messages without authentication."""
            try:
                with open(MESSAGE_FILE_PATH, 'r') as file:
                    messages = file.readlines()
                # Return messages as a JSON array
                return jsonify({'messages': [msg.strip() for msg in messages]})
            except FileNotFoundError:
                return jsonify({'message': 'Messages file not found.'}), 404

        def post(self):
            """Append a new message to the messages file."""
            data = request.get_json()
            message = data.get('message')
            if not message:
                return {'message': 'Message content is required.'}, 400
            try:
                with open(MESSAGE_FILE_PATH, 'a') as file:
                    file.write(f"{message}\n")
                return {'message': 'Message added successfully'}, 201
            except Exception as e:
                return {'message': f'Failed to add message: {str(e)}'}, 500

    # Add the resource for /messages
    api.add_resource(_Messages, '/messages')

    # Define a new endpoint for fetching trivia
    class _Trivia(Resource):
        def get(self):
            """Fetch a trivia question and append it to messages.txt."""
            topic = request.args.get('topic', '')  # Get topic from query parameters
            question = get_trivia_question(topic)

            if question:
                with open(MESSAGE_FILE_PATH, 'a') as file:
                    file.write(question + '\n')
                return jsonify({"message": "Trivia question added", "question": question})
            else:
                return jsonify({"error": "Failed to fetch trivia question"}), 500

    # Add the resource for /trivia
    api.add_resource(_Trivia, '/trivia')

def get_trivia_question(topic):
    """Fetch a trivia question from the API."""
    api_url = TRIVIA_API_URL.format(topic)
    response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
    if response.status_code == requests.codes.ok:
        question = json.loads(response.text)[0]['question']
        return question
    else:
        print("Error:", response.status_code, response.text)
        return None
