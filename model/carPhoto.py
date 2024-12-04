import base64
import os
from werkzeug.utils import secure_filename
from __init__ import app

def default_car_decode():
        img_path = f"{app.config['UPLOAD_FOLDER']}/no_car.jpg"
        with open(img_path, 'rb') as img_file:
            base64_encoded = base64.b64encode(img_file.read()).decode('utf-8')
        return base64_encoded

def car_base64_decode(user_id, user_car):
    """
    Reads a user's car picture from the server.

    This function reads a user's car picture from the server and returns the image as a base64 encoded string.
    If the user does not have a car picture set, the function returns None.

    Parameters:
    - user_id (str): The unique identifier for the user.
    - user_car (str): The filename of the user's car picture.

    Returns:
    - str: The base64 encoded image if the user has a car picture; otherwise, None.
    """
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], user_id, user_car)
    try:
        with open(img_path, 'rb') as img_file:
            base64_encoded = base64.b64encode(img_file.read()).decode('utf-8')
        return base64_encoded
    except Exception as e:
        print(f'An error occurred while reading the car picture: {str(e)}')
        return None

def car_base64_upload(base64_image, user_uid):
    """
    Uploads a base64 encoded image as a car picture for a user.

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
        filename = secure_filename(f'{user_uid}_car.png')
        user_dir = os.path.join(app.config['UPLOAD_FOLDER'], user_uid)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        file_path = os.path.join(user_dir, filename)
        with open(file_path, 'wb') as img_file:
            img_file.write(image_data)
        return filename 
    except Exception as e:
        print (f'An error occurred while updating the car picture: {str(e)}')
        return None
    
def car_file_delete(user_uid, filename):
    """
    Deletes the car picture file from the server.

    This function removes a file from the server's filesystem. It is typically used to delete car pictures
    when a user updates their image or removes it entirely.

    Parameters:
    - user_uid (str): The unique identifier for the user.
    - filename (str): The name of the file to be deleted.

    Returns:
    - bool: True if the file was deleted successfully; otherwise, False.
    """
    try:
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], user_uid, filename)
        if os.path.exists(img_path):
            os.remove(img_path)
        # Success is when the file does not exist after calling this function
        return True 
    except Exception as e:
        print(f'An error occurred while deleting the car picture: {str(e)}')
        # Failure is when the file still existes, likely a permissions issue
        return False