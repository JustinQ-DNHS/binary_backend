# post.py
from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from model.user import User

class BinaryLearningGameScores(db.Model):
    """
    Binary Learning Game Scores Model
    
    The class represents an individual contribution or discussion within a group.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the post.
    """
    __tablename__ = 'binaryLearningGameScores'

    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column(db.String(255), nullable=False)
    _user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    _user_score = db.Column(db.Integer, nullable=False)
    _user_difficulty = db.Column(db.String(255), nullable=False)

    def __init__(self, username, user_id, user_score, user_difficulty):
        """
        Constructor, 1st step in object creation.
        
        Args:
            title (str): The title of the post.
            content (str): The content of the post.
            user_id (int): The user who created the post.
            group_id (int): The group to which the post belongs.
            image_url (str): The url path to the image
        """
        self._username = username
        self._user_id = user_id
        self._user_score = user_score
        self._user_difficulty = user_difficulty

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(post) built-in function, where post is an instance of the Post class.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"BinaryScore(id={self.id}, username={self._username}, user_id={self._user_id}, user_score={self._user_score}, user_difficulty={self._user_difficulty})"

    def create(self):
        """
        The create method adds the object to the database and commits the transaction.
        
        Uses:
            The db ORM methods to add and commit the transaction.
        
        Raises:
            Exception: An error occurred when adding the object to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    def read(self):
        """
        The read method retrieves the object data from the object's attributes and returns it as a dictionary.
        
        Uses:
            The Group.query and User.query methods to retrieve the group and user objects.
        
        Returns:
            dict: A dictionary containing the post data, including user and group names.
        """
        user = User.query.get(self._user_id)
        data = {
            "id": self.id,
            "username": self._username,
            "user_id": self._user_id if user else None,
            "user_score": self._user_score,
            "user_difficulty": self._user_difficulty
        }
        return data
    
    def update(self, inputs):
        """
        The update method commits the transaction to the database.
        
        Uses:
            The db ORM method to commit the transaction.
        
        Raises:
            Exception: An error occurred when updating the object in the database.
        """
        if not isinstance(inputs, dict):
            return self

        user_score = inputs.get("user_score", "")
        user_difficulty = inputs.get("user_difficulty", "")

        if user_score:
            self._user_score = user_score
        if user_difficulty:
            self._user_difficulty = user_difficulty

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        return self
    
    def delete(self):
        """
        The delete method removes the object from the database and commits the transaction.
        
        Uses:
            The db ORM methods to delete and commit the transaction.
        
        Raises:
            Exception: An error occurred when deleting the object from the database.
        """    
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def restore(data):
        sections = {}
        existing_sections = {section._username: section for section in BinaryLearningGameScores.query.all()}
        for section_data in data:
            _ = section_data.pop('id', None)  # Remove 'id' from section_data
            username = section_data.get("username", None)
            section = existing_sections.pop(username, None)
            if section:
                section.update(section_data)
            else:
                section = BinaryLearningGameScores(**section_data)
                section.create()
        
        # Remove any extra data that is not in the backup
        for section in existing_sections.values():
            db.session.delete(section)
        
        db.session.commit()
        return sections

def initBinaryLearningGameScores():
    """
    The initPosts function creates the Post table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Post objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """
    with app.app_context():
        """Create database and tables"""
        # db.create_all()
        # """Tester data for table"""
            
        # p1 = BinaryLearningGameScores(username="JIM", user_id="1", user_score=10, user_difficulty="easy")
        # p2 = BinaryLearningGameScores(username="TIM", user_id="2", user_score=20, user_difficulty="medium")
        # p3 = BinaryLearningGameScores(username="BUM", user_id="3", user_score=30, user_difficulty="hard")
            
        # for post in [p1, p2, p3]:
        #     try:
        #         post.create()
        #         print(f"Record created: {repr(post)}")
        #     except IntegrityError:
        #         '''fails with bad or duplicate data'''
        #         db.session.remove()
        #         print(f"Records exist, duplicate email, or error: {post.user_id}")