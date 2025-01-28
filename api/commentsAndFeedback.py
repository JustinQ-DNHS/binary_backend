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
            # current_user = g.current_user
            data = request.get_json()
            # Create an empty array to append each hex code to
            hex_translate = []
            # Goes through each character and converts it to hex
            for i in range(len(data["post_id"])):
                hex_translate.append(hex(ord(data["post_id"][i]))[2:])
            # final_post_id = []
            # for i in range(len(hex_translate)):
            #     final_post_id.append(chr(int(hex_translate[i], 16)))
            # comment = CommentsAndFeedback(data['title'], data['content'], current_user.id, data['post_id'])
            comment = CommentsAndFeedback(data['title'], data['content'], ''.join(hex_translate))
            comment.create()
            return jsonify(comment.read())
        
        @token_required()
        def put(self):
            # Obtain the current user
            current_user = g.current_user
            # Obtain the request data
            data = request.get_json()
            # Find the current post from the database table(s)
            comment = CommentsAndFeedback.query.get(data['id'])
            # Update the post
            # comment._title = data['title']
            # comment._content = data['content']
            # # comment._user_id = data['user_is']
            # comment._post_id = data['post_id']
            # Save the post
            comment.update({'title': data['title'], 'content': data['content'], 'post_id': data['post_id']})
            # comment.temp_update()
            # Return response
            return jsonify(comment.read())
        
        @token_required()
        def delete(self):
            data = request.get_json()
            comment = CommentsAndFeedback.query.get(data["id"])
            comment.delete()
            return jsonify({"message": "Comment deleted"})
        
    api.add_resource(_CRUD, '/comments')