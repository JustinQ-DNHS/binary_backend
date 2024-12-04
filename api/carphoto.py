from flask import Blueprint, g, request
from flask_restful import Api, Resource
from api.jwt_authorize import token_required
from model.user import User
from model.carPhoto import car_base64_decode, car_base64_upload, car_file_delete, default_car_decode

car_api = Blueprint('car_photo_api', __name__, url_prefix='/api/id')
api = Api(car_api)

class _CarPhoto(Resource):
    """
    Retrieves the current user's Car picture as a base64 encoded string.

    This endpoint allows users to fetch their Car picture. The Car picture is returned as a base64 encoded string,
    which can be directly used in the src attribute of an img tag on the client side. This method ensures that only the
    authenticated user can access their Car picture.

    The process involves:
    1. Verifying the user's authentication and retrieving the current user object.
    2. Checking if the current user has a Car picture set.
    3. If a Car picture is set, the image file is read, and its content is base64 encoded.
    4. The base64 encoded string of the image is returned in the response.

    Returns:
    - A JSON object containing the base64 encoded string of the Car picture under the key 'car' if the operation is successful.
    - HTTP status code 200 if the Car picture is successfully retrieved.
    - HTTP status code 404 if the Car picture is not set for the current user.
    - HTTP status code 500 if an error occurs while reading the Car picture from the server.
    """
    @token_required()
    def get(self):
        current_user = g.current_user
        if not current_user.car or current_user.car == "":
            return {"message": "Car picture is not set.",
                    "car": default_car_decode()}, 404
        
        base64_encode = car_base64_decode(current_user.uid, current_user.car)

        if not base64_encode:
            return {'message': 'An error occurred while reading the car picture.'}, 500
        
        return {'car': base64_encode}, 200

    @token_required()
    def delete(self):
        """
        Deletes the user's Car picture.

        This endpoint allows for the deletion of a user's Car picture. It is restricted to users with an 'Admin' role.
        The user whose Car picture is to be deleted is identified by a 'uid' parameter in the request's query string.

        The process involves several steps:
        1. Verifying that the current user has 'Admin' privileges.
        2. Ensuring the 'uid' parameter is provided in the request.
        3. Locating the user in the database using the provided 'uid'.
        4. Checking if the user has a Car picture set.
        5. Attempting to delete the Car picture file from the server.
        6. Removing the reference to the Car picture from the user's database record.

        Returns:
        - A JSON object with a message indicating the success or failure of the operation.
        - HTTP status code 200 if the Car picture was deleted successfully.
        - HTTP status code 401 if the current user is unauthorized.
        - HTTP status code 400 if the 'uid' parameter is missing from the request.
        - HTTP status code 404 if the user is not found or if the Car picture is not set.
        - HTTP status code 500 if an error occurs during the file deletion process or while updating the database.
        """
        current_user = g.current_user

        if current_user.role != 'Admin':
            return {'message': 'Unauthorized.'}, 401

        user_uid = request.args.get('uid')
        if not user_uid:
            return {'message': 'UID required.'}, 400

        user = User.query.filter_by(_uid=user_uid).first()
        if not user:
            return {'message': 'User not found'}, 404

        if user.car:
            if not car_file_delete(user_uid, user.car):
                return {'message': 'An error occurred while deleting the Car picture, check permissions'}, 500
            
            #  Remove the user's reference to the Car picture
            try:
                user.delete_car()  # Call the delete_car method to update the database
                return {'message': 'Car picture deleted successfully'}, 200
            except Exception as e:
                return {'message': f'An error occurred while deleting the Car picture database reference: {str(e)}'}, 500
        else:
            return {'message': 'Car picture not set.'}, 404

    @token_required()
    def put(self):
        """
        Updates the user's Car picture with a new image provided as base64 encoded data.

        This endpoint allows users to update their Car picture by sending a PUT request with base64 encoded image data.
        The image is decoded and saved to a secure location on the server, and the user's profile information is updated
        to reference the new image file.

        The function requires a valid authentication token and expects the base64 image data to be included in the request's JSON body
        under the key 'car'. If the image data is not provided, or if any error occurs during the upload process or while updating
        the user's profile in the database, an appropriate error message and status code are returned.

        Returns:
        - A JSON object with a message indicating the success or failure of the operation.
        - HTTP status code 200 if the Car picture was updated successfully.
        - HTTP status code 400 if the base64 image data is missing from the request.
        - HTTP status code 500 if an error occurs during the upload process or while updating the database.
        """
        current_user = g.current_user

        # Obtain the base64 image data from the request
        if 'car' not in request.json:
            return {'message': 'Base64 image data required.'}, 400
        base64_image = request.json['car']
       
        # Make an image file from the base64 data 
        filename = car_base64_upload(base64_image, current_user.uid)
        if not filename:
            return {'message': 'An error occurred while uploading the Car picture'}, 500
        
        # Update the user's Car picture to the uploaded file
        try:
            # write the filename reference to the database
            current_user.update({"car": filename})
            return {'message': 'Car picture updated successfully'}, 200
        except Exception as e:
            return {'message': f'A database error occurred while assigning Car picture: {str(e)}'}, 500
        
api.add_resource(_CarPhoto, '/car')
