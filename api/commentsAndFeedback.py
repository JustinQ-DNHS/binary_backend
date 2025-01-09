from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource  # used for REST API building
from api.jwt_authorize import token_required
from model.commentsAndFeedback import CommentsAndFeedback

commentsAndFeedback_api = Blueprint('commentsAndFeedback_api', __name__, url_prefix='/api')

api = Api(commentsAndFeedback_api)

class CommentsAndFeedpackAPI: 
    class _CRUD(Resource):
        @token_required()
        # Fetches all comments upon a GET endpoint from the frontend and returns all the existing
        # comments in a json format
        def get(self):
            comments = CommentsAndFeedback.query.all()
            json_ready = [comment.read() for comment in comments]
            return json_ready
        @token_required()
        # Creates a new post object and adds it to the database, it then returns what it creates.
        def post(self):
            data = request.get_json()
            post = CommentsAndFeedback(data['title'], data['content'], 1, data['post_id'])
            post.create()
            return jsonify(post.read())
        
    api.add_resource(_CRUD, '/comments')