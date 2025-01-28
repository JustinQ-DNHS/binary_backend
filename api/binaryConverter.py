from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # Used for REST API building
from __init__ import app  # Ensure __init__.py initializes your Flask app
from model.binaryConverter import BinaryConverter

# Blueprint for the API
binary_converter_api = Blueprint('binary_converter_api', __name__, url_prefix='/api')

api = Api(binary_converter_api)  # Attach Flask-RESTful API to the Blueprint

class BinaryConverterAPI:
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
            # Obtain the current user
            # current_user = g.current_user
            # Find all the posts by the current user
            posts = BinaryConverter.query.all()
            # Prepare a JSON list of all the posts, uses for loop shortcut called list comprehension
            json_ready = [post.read() for post in posts]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)
        def post(self):
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Create a new post object using the data from the request
            post = BinaryConverter(data['binary'], data['decimal'])
            # Save the post object using the Object Relational Mapper (ORM) method defined in the model
            post.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(post.read())

        
        def put(self):
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            post = BinaryConverter.query.get(data['id'])
            # Update the post
            post._decimal = data['decimal']
            post._binary = data['binary']
            # Save the post
            post.update()
            # Return response
            return jsonify(post.read())
        
        def get(self):
            try:
                # Query all entries in the BinaryHistory table
                entries = BinaryConverter.query.all()
                # Convert the entries to a list of dictionaries
                results = [entry.read() for entry in entries]
                # Return the list of results in JSON format
                return jsonify(results)
            except Exception as e:
                # Return an error message in case of failure
                return jsonify({"error": str(e)}), 500
        
        
        def delete(self):
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            post = BinaryConverter.query.get(data['id'])
            # Delete the post using the ORM method defined in the model
            post.delete()
            # Return response
            return jsonify({"message": "Post deleted"})

    """
    Map the _CRUD class to the API endpoints for /post.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    """
    api.add_resource(_CRUD, '/binary-converter')
    
if __name__ == '__main__':
    app.run(debug=True)