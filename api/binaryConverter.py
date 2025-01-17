from flask import Flask, jsonify, Blueprint, request
from flask_cors import CORS
from flask_restful import Api, Resource
from __init__ import app, db
from sqlalchemy.exc import SQLAlchemyError
from api.jwt_authorize import token_required
from model.binaryConverter import BinaryConverter
# Initialize Flask app
app = Flask(__name__)

# Enable CORS for cross-origin access
CORS(app)

# Create the blueprint
binaryConverter_api = Blueprint('BinaryConverter_api', __name__, url_prefix='/api')

# Sample binary data
BINARY_CONVERTER = [
    {"binary": "1111001100001", "decimal": 7777},
    {"binary": "100100010011", "decimal": 2323},
    {"binary": "11100011010001001101", "decimal": 932237},
]

# Move the route to the blueprint
@binaryConverter_api.route('/binaryConverter', methods=['GET', 'POST'])
def binary_converter():
    if request.method == 'GET':
        """
        Endpoint to retrieve all binary history events (from static data).
        """
        return jsonify(BINARY_CONVERTER), 200

    if request.method == 'POST':
        """
        Endpoint to add a new binary conversion to the history.
        """
        data = request.json  # Parse incoming JSON
        binary_input = data.get('binary')

        # Validate binary input
        if binary_input and all(char in '01' for char in binary_input):
            decimal_value = int(binary_input, 2)  # Convert binary to decimal
            new_entry = {"binary": binary_input, "decimal": decimal_value}
            BINARY_CONVERTER.append(new_entry)  # Add to history
            return jsonify(new_entry), 201  # Return the newly added entry
        else:
            return {"error": "Invalid binary input. Only 0s and 1s are allowed."}, 400

# Register the blueprint with the app
app.register_blueprint(binaryConverter_api)

# Start the app on the desired host and port
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8887)
