from flask import Blueprint, g, request
from flask_restful import Api, Resource
from api.jwt_authorize import token_required
from model.nestPost import NestPost
from model.nestImg import nestImg_base64_decode, nestImg_base64_upload

nestImg_api = Blueprint('nestImg_api', __name__, url_prefix='/api/id')
api = Api(nestImg_api)

class _NestImage(Resource):
    """
    Retrieves the current user's profile picture as a base64 encoded string.

    This endpoint allows users to fetch their profile picture. The profile picture is returned as a base64 encoded string,
    which can be directly used in the src attribute of an img tag on the client side. This method ensures that only the
    authenticated user can access their profile picture.

    The process involves:
    1. Verifying the user's authentication and retrieving the current user object.
    2. Checking if the current user has a profile picture set.
    3. If a profile picture is set, the image file is read, and its content is base64 encoded.
    4. The base64 encoded string of the image is returned in the response.

    Returns:
    - A JSON object containing the base64 encoded string of the profile picture under the key 'pfp' if the operation is successful.
    - HTTP status code 200 if the  picture is successfully retrieved.
    - HTTP status code 404 if the  picture is not set for the current post.
    - HTTP status code 500 if an error occurs while reading the post picture from the server.
    """
    @token_required()
    def get(self):
        current_user = g.current_user
        # Doesn't work since you can't add a body to a GET
        data = request.get_json()
        current_nestPost = NestPost.query.filter_by(id=data["imageID"]).first()

        if current_nestPost._image_url:
            base64_encode = nestImg_base64_decode(current_user.uid, current_nestPost._image_url)
            if not base64_encode:
                return {'message': 'An error occurred while reading the picture.'}, 500
            return {'postImg': base64_encode}, 200
        else:
            return {'message': 'There was an error accessing the image.'}, 404

    @token_required()
    def post(self):
        current_user = g.current_user
        data = request.get_json()
        current_nestPost = NestPost.query.filter_by(id=data["imageID"]).first()

        if current_nestPost._image_url:
            base64_encode = nestImg_base64_decode(current_user.uid, current_nestPost._image_url)
            if not base64_encode:
                return {'message': 'An error occurred while reading the picture.'}, 500
            return {'postImg': base64_encode}, 200
        else:
            return {'message': 'There was an error accessing the image.'}, 404

    @token_required()
    def put(self):
        """
        Updates the user's profile picture with a new image provided as base64 encoded data.

        This endpoint allows users to update their profile picture by sending a PUT request with base64 encoded image data.
        The image is decoded and saved to a secure location on the server, and the user's profile information is updated
        to reference the new image file.

        The function requires a valid authentication token and expects the base64 image data to be included in the request's JSON body
        under the key 'pfp'. If the image data is not provided, or if any error occurs during the upload process or while updating
        the user's profile in the database, an appropriate error message and status code are returned.

        Returns:
        - A JSON object with a message indicating the success or failure of the operation.
        - HTTP status code 200 if the profile picture was updated successfully.
        - HTTP status code 400 if the base64 image data is missing from the request.
        - HTTP status code 500 if an error occurs during the upload process or while updating the database.
        """
        current_user = g.current_user
        # Grabs information and plugs it into NestPost table to get image information
        data = request.get_json()
        current_nestPost = NestPost.query.filter_by(id=data["imageID"]).first()
        
        # Obtain the base64 image data from the request
        if 'nestImg' not in request.json:
            return {'message': 'Base64 image data required.'}, 400
        base64_image = request.json['nestImg']
       
        # Make an image file from the base64 data 
        filename = nestImg_base64_upload(base64_image, current_user.uid)
        if not filename:
            return {'message': 'An error occurred while uploading the post picture'}, 500
        
        # Update the user's profile picture to the uploaded file
        try:
            # write the filename reference to the database
            current_nestPost.update({"nestImg": filename})
            return {'message': 'Post picture updated successfully'}, 200
        except Exception as e:
            return {'message': f'A database error occurred while assigning post picture: {str(e)}'}, 500
        
api.add_resource(_NestImage, '/nestImg')
