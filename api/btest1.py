import jwt
from flask import Blueprint, request, jsonify, current_app, Response, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.post import Post
from model.channel import Channel

"""
This Blueprint object is used to define APIs for the Post model.
- Blueprint is used to modularize application files.
- This Blueprint is registered to the Flask app in main.py.
"""
post_api = Blueprint('post_api', __name__, url_prefix='/api')

"""
The Api object is connected to the Blueprint object to define the API endpoints.
- The API object is used to add resources to the API.
- The objects added are mapped to code that contains the actions for the API.
- For more information, refer to the API docs: https://flask-restful.readthedocs.io/en/latest/api.html
"""
api = Api(post_api)

class PostAPI:
    """
    Define the API CRUD endpoints for the Post model.
    There are four operations that correspond to common HTTP methods:
    - post: create a new post
    - get: read posts
    - put: update a post
    - delete: delete a post
    """
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create a new post.
            """
            # Obtain the current user from the token required setting in the global context
            current_user = g.current_user
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()

            # Validate the presence of required keys
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'title' not in data:
                return {'message': 'Post title is required'}, 400
            if 'content' not in data:
                data['content'] = {}

            # Create a new post object using the data from the request
            post = Post(data['title'], data['content'])
            # Save the post object using the Object Relational Mapper (ORM) method defined in the model
            post.create()
            # Return response to the client in JSON format, converting Python dictionaries to JSON format
            return jsonify(post.read())

        @token_required()
        def get(self):
            """
            Retrieve a single post by ID.
            """
            # Obtain and validate the request data sent by the RESTful client API
            data = request.get_json()
            if data is None:
                return {'message': 'Post data not found'}, 400
            if 'id' not in data:
                return {'message': 'Post ID not found'}, 400
            # Find the post to read
            post = Post.query.get(data['id'])
            if post is None:
                return {'message': 'Post not found'}, 404
            # Convert Python object to JSON format 
            json_ready = post.read()
            # Return a JSON restful response to the client
            return jsonify(json_ready)

        @token_required()
        def put(self):
            """
            Update a post.
            """
            # Obtain the current user
            current_user = g.current_user
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            post = Post.query.get(data['id'])
            if post is None:
                return {'message': 'Post not found'}, 404
            # Update the post
            post._title = data['title']
            post._content = data['content']
            # Save the post
            post.update()
            # Return response
            return jsonify(post.read())

        @token_required()
        def delete(self):
            """
            Delete a post.
            """
            # Obtain the current user
            current_user = g.current_user
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            post = Post.query.get(data['id'])
            if post is None:
                return {'message': 'Post not found'}, 404
            # Delete the post using the ORM method defined in the model
            post.delete()
            # Return response
            return jsonify({"message": "Post deleted"})

    api.add_resource(_CRUD, '/post')