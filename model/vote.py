from __init__ import db, app
from sqlalchemy.exc import IntegrityError
from model.post import Post
from model.user import User

class Vote(db.Model):
    """
    Vote Model

    The Vote class represents a single upvote or downvote on a post by a user.

    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the vote.
        _vote_type (db.Column): A string representing the type of vote ("upvote" or "downvote").
        _user_id (db.Column): An integer representing the ID of the user who cast the vote.
        _post_id (db.Column): An integer representing the ID of the post that received the vote.
    """
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True)
    _vote_type = db.Column(db.String(10), nullable=False)  # "upvote" or "downvote"
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __init__(self, vote_type, user_id, post_id):
        """
        Constructor to initialize a vote.

        Args:
            vote_type (str): Type of the vote, either "upvote" or "downvote".
            user_id (int): ID of the user who cast the vote.
            post_id (int): ID of the post that received the vote.
        """
        self._vote_type = vote_type
        self._user_id = user_id
        self._post_id = post_id

    def create(self):
        """
        Add the vote to the database and commit the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        Retrieve the vote data as a dictionary.

        Returns:
            dict: Dictionary with vote information.
        """
        return {
            "id": self.id,
            "vote_type": self._vote_type,
            "user_id": self._user_id,
            "post_id": self._post_id
        }

    def delete(self):
        """
        Remove the vote from the database and commit the transaction.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

def initVotes():
    """
    Initialize the Vote table with any required starter data.
    """
    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()

        # Optionally, add some test data (replace with actual values as needed)
        votes = [
            Vote(vote_type='upvote', user_id=1, post_id=1),
            Vote(vote_type='downvote', user_id=2, post_id=1),
        ]
        
        for vote in votes:
            try:
                db.session.add(vote)
                db.session.commit()
                print(f"Record created: {repr(vote)}")
            except IntegrityError:
                db.session.rollback()
                print(f"Duplicate or error: {repr(vote)}")
