# feedback.py
from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from model.user import User
from model.post import Post

class Feedback(db.Model):
    """
    Feedback Model
    
    The Feedback class represents an individual contribution or discussion within a post.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the post.
        _content (db.Column): A Text blob representing the content of the post.
        _user_id (db.Column): An integer representing the user who created the post.
        _post_id (db.Column): An integer representing the post to which the post belongs.
    """
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True)
    _content = db.Column(Text, nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

    def __init__(self, content, user_id, post_id):
        """
        Constructor, 1st step in object creation.
  
            title (str): The title of the post.
            content (str): The content of the post.
            user_id (int): The user who created the post.
            post_id (int): The post to which the post belongs.
        """
        self._content = content
        self._user_id = user_id
        self._post_id = post_id

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(post) built-in function, where post is an instance of the Feedback class.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Feedback(id={self.id}, content={self._content}, user_id={self._user_id}, post_id={self._post_id})"

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
            The Post.query and User.query methods to retrieve the post and user objects.
        
        Returns:
            dict: A dictionary containing the post data, including user and post names.
        """
        user = User.query.get(self._user_id)
        post = Post.query.get(self._post_id)
        data = {
            "id": self.id,
            "content": self._content,
            "user_name": user.name if user else None,
            "post_title": post.title if post else None,
        }
        return data
    
    def update(self):
        """
        The update method commits the transaction to the database.
        
        Uses:
            The db ORM method to commit the transaction.
        
        Raises:
            Exception: An error occurred when updating the object in the database.
        """
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
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

def initFeedbacks():
    """
    The initFeedbacks function creates the Feedback table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Feedback objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """        
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        
        p1 = Feedback(title='Calculus Help', content='Need help with derivatives.', user_id=1, post_id=1)  
        p2 = Feedback(title='Game Day', content='Who is coming to the game?', user_id=2, post_id=2)
        p3 = Feedback(title='New Releases', content='What movies are you excited for?', user_id=3, post_id=3)
        p4 = Feedback(title='Study Group', content='Meeting at the library.', user_id=1, post_id=1)
        
        for post in [p1, p2, p3, p4]:
            try:
                post.create()
                print(f"Record created: {repr(post)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {post.uid}")