from flask import Blueprint, jsonify
from flask_restful import Api, Resource  # Used for REST API building
from flask_cors import CORS
from __init__ import app  # Ensure __init__.py initializes your Flask app

# Enable CORS for cross-origin access
CORS(app)

# Blueprint for the API
binary_history_api = Blueprint('binary_history_api', __name__, url_prefix='/api')

api = Api(binary_history_api)  # Attach Flask-RESTful API to the Blueprint

# Static binary history data
binaryhistory = [
    {"id": 1, "event_year": "1679", "event_description": "Gottfried Wilhelm Leibniz conceives the idea of the binary numeral system in his essay 'Explication de l'Arithmétique Binaire'."},
    {"id": 2, "event_year": "1703", "event_description": "Leibniz formally publishes his work on the binary numeral system in 'Explication de l'Arithmétique Binaire'."},
    {"id": 3, "event_year": "1847", "event_description": "George Boole develops Boolean algebra, which becomes foundational for binary logic."},
    {"id": 4, "event_year": "1854", "event_description": "George Boole publishes 'An Investigation of the Laws of Thought', further detailing Boolean algebra."},
    {"id": 5, "event_year": "1937", "event_description": "Claude Shannon applies Boolean algebra to design electronic circuits in his master's thesis."},
    {"id": 6, "event_year": "1939", "event_description": "John Atanasoff and Clifford Berry create the Atanasoff-Berry Computer (ABC), which uses binary."},
    {"id": 7, "event_year": "1945", "event_description": "John von Neumann outlines the architecture of modern computers, emphasizing binary."},
    {"id": 8, "event_year": "1946", "event_description": "The ENIAC computer is completed, though it uses decimal rather than binary."},
    {"id": 9, "event_year": "1948", "event_description": "Claude Shannon publishes 'A Mathematical Theory of Communication', linking binary to information theory."},
    {"id": 10, "event_year": "1950", "event_description": "Alan Turing's work on binary-based computation contributes to the development of modern computer science."},
    {"id": 11, "event_year": "1951", "event_description": "The UNIVAC I, the first commercial computer, uses binary in its operations."},
    {"id": 12, "event_year": "1960", "event_description": "Binary-coded decimal (BCD) becomes widely adopted for numerical representation in computing."},
    {"id": 13, "event_year": "1964", "event_description": "ASCII (American Standard Code for Information Interchange) is introduced, using binary to represent characters."},
    {"id": 14, "event_year": "1969", "event_description": "The UNIX operating system is created, relying heavily on binary representations."},
    {"id": 15, "event_year": "1971", "event_description": "Intel releases the 4004 microprocessor, the first commercially available processor based on binary."},
    {"id": 16, "event_year": "1980", "event_description": "IBM introduces the PC, making binary-based computing accessible to the public."},
    {"id": 17, "event_year": "1991", "event_description": "The World Wide Web is introduced, built upon binary protocols and systems."},
    {"id": 18, "event_year": "2000", "event_description": "The Y2K problem highlights the importance of binary in year representation and storage."},
    {"id": 19, "event_year": "2008", "event_description": "Bitcoin, based on binary and cryptographic principles, is introduced."},
    {"id": 20, "event_year": "2020", "event_description": "Quantum computing advancements begin to challenge traditional binary systems with qubits."}
];

# Create a class for the Binary History API
class BinaryHistoryAPI:
    """
    Define the API CRUD endpoints for Binary History.
    """

    class _GetAll(Resource):
        def get(self):
            """
            Retrieve all binary history events.
            """
            return jsonify(binaryhistory)  # Convert Python list to JSON and return it

    # Add resource to the API
    api.add_resource(_GetAll, '/binary-history')

if __name__ == '__main__':
    app.run(debug=True)