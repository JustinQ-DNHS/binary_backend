from flask import Flask, jsonify, Blueprint

app = Flask(__name__)

binary_history_api = Blueprint('binary_history_api', __name__, url_prefix='/api')

# Static binary history data
BINARY_HISTORY = [
    {"id": 1, "event_date": "1703-01-01", "event_description": "Gottfried Wilhelm Leibniz develops the binary numeral system."},
    {"id": 2, "event_date": "1937-01-01", "event_description": "Claude Shannon applies Boolean algebra to electronic circuits."},
    {"id": 3, "event_date": "1945-01-01", "event_description": "John von Neumann describes the binary architecture of modern computers."},
    {"id": 4, "event_date": "1964-01-01", "event_description": "ASCII (American Standard Code for Information Interchange) is introduced, using binary to represent characters."},
]

# Define route for the blueprint
@binary_history_api.route('/binary-history', methods=['GET'])
def get_binary_history():
    """
    Endpoint to retrieve all binary history events (from static data).
    """
    return jsonify(BINARY_HISTORY), 200

if __name__ == '__main__':
    app.run(debug=True)