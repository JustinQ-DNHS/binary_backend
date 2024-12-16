from flask import Blueprint, request, jsonify
from models.quizgrading import NestPost
from sqlalchemy.exc import IntegrityError
from __init__ import db

# Create a Blueprint for this API
quizgrading_bp = Blueprint('quizgrading', __name__)

@quizgrading_bp.route('/api/posts', methods=['GET'])
def get_all_posts():
    """
    GET method to fetch all the posts in the database and return as JSON.
    """
    try:
        posts = NestPost.query.all()  # Retrieve all posts from the database
        posts_data = [post.read() for post in posts]  # Call the 'read' method to format data
        return jsonify(posts_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@quizgrading_bp.route('/api/posts', methods=['POST'])
def create_post():
    """
    POST method to create a new post in the database. The request body should include:
    - title
    - content
    - user_id
    - group_id
    - image_url
    """
    try:
        # Extract data from the request body
        data = request.get_json()

        # Check if all required fields are present
        if not all(key in data for key in ['title', 'content', 'user_id', 'group_id', 'image_url']):
            return jsonify({"error": "Missing required fields"}), 400

        # Create a new NestPost object
        new_post = NestPost(
            title=data['title'],
            content=data['content'],
            user_id=data['user_id'],
            group_id=data['group_id'],
            image_url=data['image_url']
        )

        # Add and commit the new post to the database
        new_post.create()
        return jsonify(new_post.read()), 201  # Return the created post as JSON with a 201 status code

    except IntegrityError as e:
        db.session.rollback()  # Rollback in case of an error
        return jsonify({"error": "Integrity error, likely a duplicate entry"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Register the blueprint with the Flask app
def register_quizgrading_api(app):
    app.register_blueprint(quizgrading_bp)
