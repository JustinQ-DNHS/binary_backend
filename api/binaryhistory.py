from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # Used for REST API building
from __init__ import app  # Ensure __init__.py initializes your Flask app
from model.binaryhistory import BinaryHistory

# Blueprint for the API
binary_history_api = Blueprint('binary_history_api', __name__, url_prefix='/api')

api = Api(binary_history_api)  # Attach Flask-RESTful API to the Blueprint

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
        def get(self):
            try:
                # Query all entries in the BinaryHistory table
                entries = BinaryHistory.query.all()
                # Convert the entries to a list of dictionaries
                results = [entry.read() for entry in entries]
                # Return the list of results in JSON format
                return jsonify(results)
            except Exception as e:
                # Return an error message in case of failure
                return jsonify({"error": str(e)}), 500
        
        def post(self):
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Create a new post object using the data from the request
            post = BinaryHistory(data['year'], data['description'])
            # Save the post object using the Object Relational Mapper (ORM) method defined in the model
            post.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(post.read())
        
        def put(self):
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            post = BinaryHistory.query.get(data['id'])
            # Update the post
            post.year = data['year']
            post.description = data['description']
            # Save the post
            post.update()
            # Return response
            return jsonify(post.read())

        
        def delete(self):
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            post = BinaryHistory.query.get(data['id'])
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