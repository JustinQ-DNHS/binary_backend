from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # Used for REST API building
from flask_cors import CORS
from __init__ import app  # Ensure __init__.py initializes your Flask app
from api.jwt_authorize import token_required
from model.nestPost import NestPost

# Enable CORS for cross-origin access
CORS(app)

# Blueprint for the API
binary_history_api = Blueprint('binary_history_api', __name__, url_prefix='/api')

api = Api(binary_history_api)  # Attach Flask-RESTful API to the Blueprint

# Static binary history data
binaryhistory = [
    {"id": 1, "year": "1679", "description": "Gottfried Wilhelm Leibniz conceives the idea of the binary numeral system in his essay 'Explication de l'Arithmétique Binaire'."},
    {"id": 2, "year": "1703", "description": "Leibniz formally publishes his work on the binary numeral system in 'Explication de l'Arithmétique Binaire'."},
    {"id": 3, "year": "1847", "description": "George Boole develops Boolean algebra, which becomes foundational for binary logic."},
    {"id": 4, "year": "1854", "description": "George Boole publishes 'An Investigation of the Laws of Thought', further detailing Boolean algebra."},
    {"id": 5, "year": "1937", "description": "Claude Shannon applies Boolean algebra to design electronic circuits in his master's thesis."},
    {"id": 6, "year": "1939", "description": "John Atanasoff and Clifford Berry create the Atanasoff-Berry Computer (ABC), which uses binary."},
    {"id": 7, "year": "1945", "description": "John von Neumann outlines the architecture of modern computers, emphasizing binary."},
    {"id": 8, "year": "1946", "description": "The ENIAC computer is completed, though it uses decimal rather than binary."},
    {"id": 9, "year": "1948", "description": "Claude Shannon publishes 'A Mathematical Theory of Communication', linking binary to information theory."},
    {"id": 10, "year": "1950", "description": "Alan Turing's work on binary-based computation contributes to the development of modern computer science."},
    {"id": 11, "year": "1951", "description": "The UNIVAC I, the first commercial computer, uses binary in its operations."},
    {"id": 12, "year": "1960", "description": "Binary-coded decimal (BCD) becomes widely adopted for numerical representation in computing."},
    {"id": 13, "year": "1964", "description": "ASCII (American Standard Code for Information Interchange) is introduced, using binary to represent characters."},
    {"id": 14, "year": "1969", "description": "The UNIX operating system is created, relying heavily on binary representations."},
    {"id": 15, "year": "1971", "description": "Intel releases the 4004 microprocessor, the first commercially available processor based on binary."},
    {"id": 16, "year": "1980", "description": "IBM introduces the PC, making binary-based computing accessible to the public."},
    {"id": 17, "year": "1991", "description": "The World Wide Web is introduced, built upon binary protocols and systems."},
    {"id": 18, "year": "2000", "description": "The Y2K problem highlights the importance of binary in year representation and storage."},
    {"id": 19, "year": "2008", "description": "Bitcoin, based on binary and cryptographic principles, is introduced."},
    {"id": 20, "year": "2020", "description": "Quantum computing advancements begin to challenge traditional binary systems with qubits."}
]

class BinaryHistoryAPI:
    """
    Define the API CRUD endpoints for the Post model.
    There are four operations that correspond to common HTTP methods:
    - post: create a new post
    - get: read posts
    - put: update a post
    - delete: delete a post
    """
    class _CRUD(Resource):
        @token_required()
        def post(self):
            # Obtain the current user from the token required setting in the global context
            current_user = g.current_user
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Create a new post object using the data from the request
            post = NestPost(data['year'], data['description'], current_user.id)
            # Save the post object using the Object Relational Mapper (ORM) method defined in the model
            post.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(post.read())

        @token_required()
        def get(self):
            # Obtain the current user
            current_user = g.current_user
            # Find all the posts by the current user
            posts = NestPost.query.filter(NestPost._user_id == current_user.id).all()
            # Prepare a JSON list of all the posts, uses for loop shortcut called list comprehension
            json_ready = [post.read() for post in posts]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready) and jsonify(binaryhistory)

        @token_required()
        def put(self):
            # Obtain the current user
            current_user = g.current_user
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            post = NestPost.query.get(data['id'])
            # Update the post
            post._title = data['title']
            post._content = data['content']
            post._group_id = data['group_id']
            post._image_url = data['image_url']
            # Save the post
            post.update()
            # Return response
            return jsonify(post.read())

        @token_required()
        def delete(self):
            # Obtain the current user
            current_user = g.current_user
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            post = NestPost.query.get(data['id'])
            # Delete the post using the ORM method defined in the model
            post.delete()
            # Return response
            return jsonify({"message": "Post deleted"})

    """
    Map the _CRUD class to the API endpoints for /post.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    """
    api.add_resource(_CRUD, '/binary-history')
    
if __name__ == '__main__':
    app.run(debug=True)