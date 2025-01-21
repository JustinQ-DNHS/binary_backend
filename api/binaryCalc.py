from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # Used for REST API building
from __init__ import app  # Ensure __init__.py initializes your Flask app
from model.binaryCalc import binaryCalc

# Blueprint for the API
binary_calc_api = Blueprint('binary_calc_api', __name__, url_prefix='/api')

api = Api(binary_calc_api)  # Attach Flask-RESTful API to the Blueprint


class binaryCalcAPI:
    # Counter variable
    decimal = {"value": 0}


    @app.route('/increment', methods=['POST'])
    def increment_counter():
        """Increments the counter by 1"""
        decimal["value"] += 1
        return jsonify(decimal)


    @app.route('/get-counter', methods=['GET'])

    def get_counter():
        # Extract the integer value from the dictionary
        decimal_extracted = decimal["value"]  # Get the integer from the dictionary
        InfoDb = []
        binary_variable = bin(decimal_extracted)  # Binary conversion (string with '0b' prefix)
        octal_variable = oct(decimal_extracted)   # Octal conversion (string with '0o' prefix)
        hexadecimal_variable = hex(decimal_extracted)  # Hexadecimal conversion (string with '0x' prefix)
        InfoDb.append({
            "decimal": decimal,
            "binary": binary_variable,
            "octal": octal_variable,
            "hexadecimal": hexadecimal_variable
        })
        """Returns the current counter value."""
        return jsonify(InfoDb)


    if __name__ == '__main__':
            app.run(debug=True)


