from flask import Blueprint, request, jsonify, g
from flask_restful import Api, Resource  # used for REST API building
from api.jwt_authorize import token_required
from model.commentsAndFeedback import CommentsAndFeedback

commentsAndFeedback_api = Blueprint('commentsAndFeedback_api', __name__, url_prefix='/api')

api = Api(commentsAndFeedback_api)

class CommentsAndFeedpackAPI: 
    class _CRUD(Resource):
        @token_required()
        def get(self):
            comments = CommentsAndFeedback.query.all()
            json_ready = [comment.read() for comment in comments]
            return json_ready
        @token_required()
        def post(self):
            # Obtain the current user from the token
            current_user = g.current_user
            # Obtain the request data sent by the RESTful client API
            data = request.get_json()
            # Create a new post object using the data from the request
            post = CommentsAndFeedback(data['title'], data['content'], 1, 1)
            # Save the post object using the ORM method defined in the model
            post.create()
            # Return response to the client in JSON format
            return jsonify(post.read())
        
    api.add_resource(_CRUD, '/comments')