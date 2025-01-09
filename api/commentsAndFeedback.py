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
        
    api.add_resource(_CRUD, '/comments')