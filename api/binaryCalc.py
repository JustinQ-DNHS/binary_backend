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


    # Endpoint to increment the counter
    @app.route('/increment', methods=['POST'])
    def increment_counter():
        """Increments the counter by 1"""
        decimal["value"] += 1
        return jsonify(decimal)


    # Endpoint to get the current counter value and its conversions
    @app.route('/get-counter', methods=['GET'])
    def get_counter():
        """Returns the current counter value and its conversions."""
        decimal_value = decimal["value"]
        binary_value = bin(decimal_value)[2:]  # Binary conversion without '0b'
        octal_value = oct(decimal_value)[2:]   # Octal conversion without '0o'
        hexadecimal_value = hex(decimal_value)[2:].upper()  # Hexadecimal without '0x'

        return jsonify({
            "decimal": decimal_value,
            "binary": binary_value,
            "octal": octal_value,
            "hexadecimal": hexadecimal_value
        })


    # Endpoint to add a new binary calculation
    @app.route('/calculations', methods=['POST'])
    def add_calculation():
        """Adds a new binary calculation."""
        data = request.json
        user_id = data.get('user_id')
        binary_value = data.get('binary_value')

        # Validate binary input
        if not binary_value or not isinstance(binary_value, int):
            return jsonify({"error": "Invalid binary value. Must be an integer."}), 400

        # Convert binary to decimal
        decimal_value = int(str(binary_value), 2)

        # Create a new binaryCalc record
        new_calc = binaryCalc(user_id=user_id, binary_value=binary_value, decimal_value=decimal_value)
        try:
            new_calc.create()
            return jsonify(new_calc.read()), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # Endpoint to retrieve all calculations
    @app.route('/calculations', methods=['GET'])
    def get_calculations():
        """Returns all stored calculations."""
        try:
            calculations = binaryCalc.query.all()
            return jsonify([calc.read() for calc in calculations])
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # Endpoint to retrieve a specific calculation by ID
    @app.route('/calculations/<int:id>', methods=['GET'])
    def get_calculation(id):
        """Returns a specific calculation by ID."""
        calculation = binaryCalc.query.get_or_404(id)
        return jsonify(calculation.read())


    # Endpoint to delete a calculation by ID
    @app.route('/calculations/<int:id>', methods=['DELETE'])
    def delete_calculation(id):
        """Deletes a specific calculation by ID."""
        calculation = binaryCalc.query.get_or_404(id)
        try:
            calculation.delete()
            return jsonify({"message": "Calculation deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # Endpoint to initialize the database with sample data
    @app.route('/init-db', methods=['POST'])
    def init_db():
        """Initializes the database with sample binary calculations."""
        try:
            initBinaryCalc()
            return jsonify({"message": "Database initialized with sample data."}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)


