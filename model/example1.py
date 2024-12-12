# post.py
# post.py
from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from model.user import User
from model.group import Group

class Example(db.Model):
    """
    Example Model
    
    The Post class represents an individual contribution or discussion within a group.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the post.
        _first_name (db.Column): A string representing the first_name of the post.
        _last_name (db.Column): A Text blob representing the last_name of the post.
    """
    __tablename__ = 'Example'

    id = db.Column(db.Integer, primary_key=True)
    _first_name = db.Column(db.String(255), nullable=False)
    _last_name = db.Column(Text, nullable=False)

    def __init__(self, first_name, last_name):
        """
        Constructor, 1st step in object creation.
        
        Args:
            first_name (str): The first_name of the post.
            last_name (str): The last_name of the post.
        """
        self._first_name = first_name
        self._last_name = last_name

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(post) built-in function, where post is an instance of the Post class.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Post(id={self.id}, first_name={self._first_name}, last_name={self._last_name})"

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
        data = {
            "id": self.id,
            "first_name": self._first_name,
            "last_name": self._last_name,
            # Review information as this may not work as this is a quick workaround
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

def initExamples():
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
        db.create_all()
        """Tester data for table"""
        
        p1 = Example(first_name='Calculus Help', last_name='Need help with derivatives.')  
        p2 = Example(first_name='Game Day', last_name='Who is coming to the game?')
        p3 = Example(first_name='New Releases', last_name='What movies are you excited for?')
        p4 = Example(first_name='Study Group', last_name='Meeting at the library.')
        
        for post in [p1, p2, p3, p4]:
            try:
                post.create()
                print(f"Record created: {repr(post)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {post.uid}")