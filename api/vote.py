import jwt
from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource  # used for REST API building
from datetime import datetime
from __init__ import app
from api.jwt_authorize import token_required
from model.post import Post
from model.vote import Vote

# Define the Blueprint for the Vote API
vote_api = Blueprint('vote_api', __name__, url_prefix='/api')

# Connect the Api object to the Blueprint
api = Api(vote_api)

class VoteAPI:
    """
    Define the API CRUD endpoints for the Vote model.
    There are operations for upvoting, downvoting, and retrieving votes for a post.
    """

    class _CRUD(Resource):
        @token_required()
        def post(self):
            """
            Create or update a vote (upvote or downvote) for a post.
            """
            # Get current user from the token
            current_user = g.current_user
            # Get the request data
            data = request.get_json()

            # Validate required fields
            if not data:
                return {'message': 'No input data provided'}, 400
            if 'post_id' not in data:
                return {'message': 'Post ID is required'}, 400
            if 'vote_type' not in data or data['vote_type'] not in ['upvote', 'downvote']:
                return {'message': 'Vote type must be "upvote" or "downvote"'}, 400

            # Check if the vote already exists for the user on the post
            existing_vote = Vote.query.filter_by(_post_id=data['post_id'], _user_id=current_user.id).first()
            if existing_vote:
                # Update the existing vote type
                existing_vote._vote_type = data['vote_type']
                existing_vote.create()  # This will commit the update
                return jsonify(existing_vote.read())

            # Create a new vote object
            vote = Vote(data['vote_type'], current_user.id, data['post_id'])
            # Save the vote using the ORM method
            vote.create()
            # Return the saved vote in JSON format
            return jsonify(vote.read())

        @token_required()
        def delete(self):
            """
            Remove a vote by a user on a specific post.
            """
            # Get current user from the token
            current_user = g.current_user
            # Get the request data
            data = request.get_json()

            # Validate required fields
            if not data or 'post_id' not in data:
                return {'message': 'Post ID is required'}, 400

            # Find the vote by user and post
            vote = Vote.query.filter_by(_post_id=data['post_id'], _user_id=current_user.id).first()
            if vote is None:
                return {'message': 'Vote not found'}, 404

            # Delete the vote
            vote.delete()
            return jsonify({"message": "Vote removed"})

    class _POST_VOTES(Resource):
        def get(self):
            """
            Retrieve all votes for a specific post, including counts of upvotes and downvotes.
            """
            # Attempt to get post_id from query parameters first
            post_id = request.args.get('post_id')
            
            # If not found in query params, try to parse from JSON body
            if not post_id:
                try:
                    data = request.get_json()
                    post_id = data.get('post_id') if data else None
                except:
                    return {'message': 'Post ID is required either as a query parameter or in the JSON body'}, 400

            if not post_id:
                return {'message': 'Post ID is required'}, 400

            # Get all votes for the post
            votes = Vote.query.filter_by(_post_id=post_id).all()
            upvotes = [vote.read() for vote in votes if vote._vote_type == 'upvote']
            downvotes = [vote.read() for vote in votes if vote._vote_type == 'downvote']

            result = {
                "post_id": post_id,
                "upvote_count": len(upvotes),
                "downvote_count": len(downvotes),
                "upvotes": upvotes,
                "downvotes": downvotes
            }
            return jsonify(result)

    """
    Map the _CRUD and _POST_VOTES classes to the API endpoints for /vote and /vote/post.
    - The _CRUD class defines the HTTP methods for voting (post and delete).
    - The _POST_VOTES class defines the endpoint for retrieving all votes for a specific post.
    """
    api.add_resource(_CRUD, '/vote')
    api.add_resource(_POST_VOTES, '/vote/post')
