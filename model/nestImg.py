import base64
import os
from werkzeug.utils import secure_filename
from __init__ import app

def nestImg_base64_decode(user_id, imageURL):
    """
    Reads a user's profile picture from the server.

    This function reads a user's profile picture from the server and returns the image as a base64 encoded string.
    If the user does not have a profile picture set, the function returns None.

    Parameters:
    - user_id (str): The unique identifier for the user.
    - user_pfp (str): The filename of the user's profile picture.

    Returns:
    - str: The base64 encoded image if the user has a profile picture; otherwise, None.
    """
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], user_id, imageURL)
    try:
        with open(img_path, 'rb') as img_file:
            base64_encoded = base64.b64encode(img_file.read()).decode('utf-8')
        return base64_encoded
    except Exception as e:
        print(f'An error occurred while reading the post picture: {str(e)}')
        return None

def nestImg_base64_upload(base64_image, user_uid):
    """
    Uploads a base64 encoded image as a profile picture for a user.

    This function decodes a base64 encoded image and saves it to a secure location on the server.
    It organizes images by storing each user's image in a separate directory within the UPLOAD_FOLDER.
    This approach helps to avoid filename conflicts and ensures better organization of files.

    Parameters:
    - base64_image (str): The base64 encoded image to be uploaded.
    - user_uid (str): The unique identifier for the user.

    Returns:
    - str: The filename of the saved image if the upload is successful; otherwise, None.
    """
    try:
        image_data = base64.b64decode(base64_image)
        filename = secure_filename(f'{user_uid}.png')
        user_dir = os.path.join(app.config['UPLOAD_FOLDER'], user_uid)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        file_path = os.path.join(user_dir, filename)
        with open(file_path, 'wb') as img_file:
            img_file.write(image_data)
        return filename 
    except Exception as e:
        print (f'An error occurred while updating the post picture: {str(e)}')
        return None