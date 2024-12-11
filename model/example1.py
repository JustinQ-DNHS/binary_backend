# post.py
from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from model.user import User
from model.group import Group

class NestPost(db.Model):
    """
    NestPost Model
    
    The Post class represents an individual contribution or discussion within a group.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the post.
        _title (db.Column): A string representing the title of the post.
        _content (db.Column): A Text blob representing the content of the post.
        _user_id (db.Column): An integer representing the user who created the post.
        _group_id (db.Column): An integer representing the group to which the post belongs.
        _image_url (db.Column): A string representing the url path to the image contained in the post
    """
    __tablename__ = 'nestPosts'

    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), nullable=False)
    _content = db.Column(Text, nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    _group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    _image_url = db.Column(db.String(255), nullable=False)

    def __init__(self, title, content, user_id, group_id, image_url):
        """
        Constructor, 1st step in object creation.
        
        Args:
            title (str): The title of the post.
            content (str): The content of the post.
            user_id (int): The user who created the post.
            group_id (int): The group to which the post belongs.
            image_url (str): The url path to the image
        """
        self._title = title
        self._content = content
        self._user_id = user_id
        self._group_id = group_id
        self._image_url = image_url

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(post) built-in function, where post is an instance of the Post class.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Post(id={self.id}, title={self._title}, content={self._content}, user_id={self._user_id}, group_id={self._group_id}, image_url={self._image_url})"

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
        group = Group.query.get(self._group_id)
        data = {
            "id": self.id,
            "title": self._title,
            "content": self._content,
            "user_name": user.name if user else None,
            "group_name": group.name if group else None,
            # Review information as this may not work as this is a quick workaround
            "image_url": self._image_url
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

def initNestPosts():
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
        
        p1 = NestPost(title='Calculus Help', content='Need help with derivatives.', user_id=1, group_id=1, image_url="toby1.png")  
        p2 = NestPost(title='Game Day', content='Who is coming to the game?', user_id=2, group_id=2, image_url="toby2.png")
        p3 = NestPost(title='New Releases', content='What movies are you excited for?', user_id=3, group_id=3, image_url="toby3.png")
        p4 = NestPost(title='Study Group', content='Meeting at the library.', user_id=1, group_id=1, image_url="toby4.png")
        
        for post in [p1, p2, p3, p4]:
            try:
                post.create()
                print(f"Record created: {repr(post)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {post.uid}")