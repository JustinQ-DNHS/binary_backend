from flask import Flask, jsonify, Blueprint, request
from flask_cors import CORS
from flask_restful import Api, Resource
from __init__ import app, db
from sqlalchemy.exc import SQLAlchemyError
from api.jwt_authorize import token_required
from model.binaryConverter import BinaryConverter

app = Flask(__name__)


CORS(app)  # Enable CORS for cross-origin access


binaryConverter_api = Blueprint('binaryConverter_api', __name__, url_prefix='/api')
  
BINARY_CONVERTER = [
   {"decimal": 5, "binary": "101"},
       {"decimal": 10, "binary": "1010"},
       {"decimal": 15, "binary": "1111"},
       {"decimal": 20, "binary": "10100"},
       {"decimal": 42, "binary": "101010"},
       {"decimal": 255, "binary": "11111111"},
   ]

# Define route for the blueprint
@binaryConverter_api.route('/binaryConverter', methods=['GET'])
def get_binaryConverter():
   """
   Endpoint to retrieve all binary history events (from static data).
   """
   return jsonify(BINARY_CONVERTER), 200


if __name__ == '__main__':
   app.run(debug=True)




