from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # Used for REST API building
from __init__ import app  # Ensure __init__.py initializes your Flask app
from model.lgatedata import lgate

# Blueprint for the API
lgate_api = Blueprint('lgate_api', __name__, url_prefix='/api')

api = Api(lgate_api)  # Attach Flask-RESTful API to the Blueprint

class LGateAPI:
    """
    Define the API CRUD endpoints for the Post model.
    There are four operations that correspond to common HTTP methods:
    - post: create a new post
    - get: read posts
    - put: update a post
    - delete: delete a post
    """
    class _CRUD(Resource):
        def post(self):
            data = request.get_json()
            # Create a new post object using the data from the request
            post = lgate(data['name'], data['score'])
            # Save the post object using the Object Relational Mapper (ORM) method defined in the model
            post.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(post.read())
        
        def get(self):
            # Obtain the current user
            # current_user = g.current_user
            # Find all the posts by the current user
            posts = lgate.query.all()
            # Prepare a JSON list of all the posts, uses for loop shortcut called list comprehension
            json_ready = [post.read() for post in posts]
            # Return a JSON list, converting Python dictionaries to JSON format
            return jsonify(json_ready)
        
        def put(self):
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            post = lgate.query.get(data['id'])
            # Update the post
            post._name = data['name']
            post._score = data['score']
            # Save the post
            post.update()
            # Return response
            return jsonify(post.read())

        
        def delete(self):
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            post = lgate.query.get(data['id'])
            # Delete the post using the ORM method defined in the model
            post.delete()
            # Return response
            return jsonify({"message": "Post deleted"})

    """
    Map the _CRUD class to the API endpoints for /post.
    - The API resource class inherits from flask_restful.Resource.
    - The _CRUD class defines the HTTP methods for the API.
    """
    api.add_resource(_CRUD, '/lgate')
    
if __name__ == '__main__':
    app.run(debug=True)