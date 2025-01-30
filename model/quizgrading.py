from sqlite3 import IntegrityError
from __init__ import app, db
from model.user import User

class quizgrading(db.Model):
    __tablename__ = 'quizgrading'

    id = db.Column(db.Integer, primary_key=True)
    _quizgrade = db.Column(db.String, nullable=False)
    _attempt = db.Column(db.String, nullable=False)

    def __init__(self, quizgrade, attempt):

        self._quizgrade = quizgrade
        self._attempt = attempt

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(post) built-in function, where post is an instance of the Post class.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"<quizgrading(id={self.id}, quizgrade={self._quizgrade}, attempt={self._attempt})>"

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
            "quizgrade": self._quizgrade,
            "attempt": self._attempt,
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

def initquizgrading():
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
        
        entries = [
            quizgrading(quizgrade=50, attempt=1),  
            quizgrading(quizgrade=60, attempt=2),
            quizgrading(quizgrade=70, attempt=3),
            quizgrading(quizgrade=80, attempt=4)
        ]
        for entry in entries:
            try:
                db.session.add(entry)
                db.session.commit()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.rollback()
                print(f"Record creation failed: {entry}")