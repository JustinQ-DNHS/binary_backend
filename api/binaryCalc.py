from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # Used for REST API building
from __init__ import app, db # Ensure __init__.py initializes your Flask app
from model.binaryCalc import binaryCalc
from flask_cors import CORS
CORS(app)

# Blueprint for the API
binary_calc_api = Blueprint('binary_calc_api', __name__, url_prefix='/api')

api = Api(binary_calc_api)  # Attach Flask-RESTful API to the Blueprint

def calculate_conversions(value):
    """Helper function to calculate binary, octal, and hexadecimal."""
    return {
        "binary": bin(value)[2:].zfill(8),  # Binary with 8 bits
        "octal": oct(value)[2:],  # Octal representation
        "hexadecimal": hex(value)[2:].upper(),  # Hexadecimal representation
        "decimal": value,  # Decimal value
    }

class binaryCalcAPI:

    @app.route('/increment', methods=['POST'])
    def increment_counter():
        """Increments the counter value in the database."""
        calc = binaryCalc.query.first()
        if not calc:
            return jsonify({"error": "Counter not initialized in the database."}), 400

        calc._decimal_value += 1
        try:
            calc.update()
            conversions = calculate_conversions(calc._decimal_value)
            return jsonify(conversions)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/reset', methods=['POST'])
    def reset_decimal():
        """Reset the decimal value to 0 in the database."""
        calc = binaryCalc.query.first()
        if not calc:
            return jsonify({"error": "Counter not initialized in the database."}), 400

        calc._decimal_value = 0
        try:
            calc.update()
            conversions = calculate_conversions(calc._decimal_value)
            return jsonify(conversions), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/get-counter', methods=['GET'])
    def get_counter():
        """Fetch the current counter value from the database."""
        calc = binaryCalc.query.first()
        if not calc:
            return jsonify({"error": "Counter not initialized in the database."}), 400

        conversions = calculate_conversions(calc._decimal_value)
        return jsonify(conversions)

    @app.route('/decrement', methods=['POST'])
    def decrement_counter():
        """Decrements the counter value in the database."""
        calc = binaryCalc.query.first()
        if not calc:
            return jsonify({"error": "Counter not initialized in the database."}), 400

        calc._decimal_value -= 1
        try:
            calc.update()
            conversions = calculate_conversions(calc._decimal_value)
            return jsonify(conversions)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/update-counter', methods=['PUT'])
    def update_counter():
        """Updates the counter to a specific value provided in the request."""
        data = request.get_json()
        new_value = data.get('value')

        if new_value is None or not isinstance(new_value, int):
            return jsonify({"error": "Invalid value. Please provide an integer."}), 400

        if new_value < 0:
            return jsonify({"error": "Value must be a non-negative integer."}), 400

        calc = binaryCalc.query.first()
        if not calc:
            return jsonify({"error": "Counter not initialized in the database."}), 400

        calc._decimal_value = new_value
        try:
            calc.update()
            conversions = calculate_conversions(new_value)
            return jsonify({"value": new_value, **conversions}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Failed to update counter: {str(e)}"}), 500

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


