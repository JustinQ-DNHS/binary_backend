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
BINARY_HISTORY = [
    {"id": 1, "event_date": "1703-01-01", "event_description": "Gottfried Wilhelm Leibniz develops the binary numeral system."},
    {"id": 2, "event_date": "1937-01-01", "event_description": "Claude Shannon applies Boolean algebra to electronic circuits."},
    {"id": 3, "event_date": "1945-01-01", "event_description": "John von Neumann describes the binary architecture of modern computers."},
    {"id": 4, "event_date": "1964-01-01", "event_description": "ASCII (American Standard Code for Information Interchange) is introduced, using binary to represent characters."},
]

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
            return jsonify(BINARY_HISTORY)  # Convert Python list to JSON and return it

    # Add resource to the API
    api.add_resource(_GetAll, '/binary-history')

if __name__ == '__main__':
    app.run(debug=True)