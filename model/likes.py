# likes.py
from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from model.post import Post

class Likes(db.Model):
    """
    Likes Model
    
    The Likes class represents an individual contribution or discussion within a group.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the likes.
        _likes(db.Column): A string representing the likes of the likes.
        _dislikes (db.Column): A Text blob representing the dislikes of the likes.
        _post_id (db.Column): An integer representing the likes who created the likes.
    """
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    _likes = db.Column(db.String(255), nullable=False)
    _dislikes = db.Column(Text, nullable=False)
    _post_id = db.Column(db.Integer, db.ForeignKey('likes.id'), nullable=False)

    def __init__(self, likes, dislikes, post_id):
        """
        Constructor, 1st step in object creation.
        
        Args:
            likes (str): The likes of the post.
            dislikes (str): The dislikes of the post.
            post_id (int): The likes who created the post.
        """
        self._likes = likes
        self._dislikes = dislikes
        self._post_id = post_id

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(post) built-in function, where post is an instance of the Likes class.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Likes(id={self.id}, likes={self._likes}, dislikes={self._dislikes}, post_id={self._post_id})"

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
            The Group.query and Likes.query methods to retrieve the group and post objects.
        
        Returns:
            dict: A dictionary containing the likes data, including post and group names.
        """
        likes = Likes.query.get(self._post_id)
        data = {
            "id": self.id,
            "likes": self._likes,
            "dislikes": self._dislikes,
            "posts_id": likes.name if likes else None,
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

def initLikes():
    """
    The initLikes function creates the Likes table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Likes objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """        
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        
        p1 = Likes(likes='Calculus Help', dislikes='Need help with derivatives.', post_id=1)  
        p2 = Likes(likes='Game Day', dislikes='Who is coming to the game?', post_id=2)
        p3 = Likes(likes='New Releases', dislikes='What movies are you excited for?', post_id=3)
        p4 = Likes(likes='Study Group', dislikes='Meeting at the library.', post_id=1)
        
        for post in [p1, p2, p3, p4]:
            try:
                post.create()
                print(f"Record created: {repr(post)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {post.uid}")