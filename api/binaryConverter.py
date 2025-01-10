from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin access
@app.route('/api/binary-converter', methods=['GET'])
def get_binary_examples():
    # Predefined examples for binary conversion
    binary_examples = [
        {"decimal": 5, "binary": "101"},
        {"decimal": 10, "binary": "1010"},
        {"decimal": 15, "binary": "1111"},
        {"decimal": 20, "binary": "10100"},
        {"decimal": 42, "binary": "101010"},
        {"decimal": 255, "binary": "11111111"},
    ]
    return jsonify(binary_examples)
if __name__ == '__main__':
    app.run(debug=True)