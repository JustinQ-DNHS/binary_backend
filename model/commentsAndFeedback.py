# post.py
from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from model.user import User

class CommentsAndFeedback(db.Model):
    """
    NestPost Model
    
    The Post class represents an individual contribution or discussion within a group.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the post.
        _title (db.Column): A string representing the title of the post.
        _content (db.Column): A Text blob representing the content of the post.
        _user_id (db.Column): An integer representing the user who created the post.
        _group_id (db.Column): An integer representing the group to which the post belongs.
    """
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    _title = db.Column(db.String(255), nullable=False)
    _content = db.Column(Text, nullable=False)
    # _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # _post_id = db.Column(db.String(255), nullable=False, unique=True)
    _post_id = db.Column(db.String(255), nullable=False)

    # def __init__(self, title, content, user_id, post_id):
    def __init__(self, title, content, post_id):
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
        # self._user_id = user_id
        self._post_id = post_id

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(post) built-in function, where post is an instance of the Post class.
        
        Returns:
            str: A text representation of how to create the object.
        """
        # return f"Post(id={self.id}, title={self._title}, content={self._content}, user_id={self._user_id}, post_id={self._post_id})"
        return f"Post(id={self.id}, title={self._title}, content={self._content}, post_id={self._post_id})"

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
        # user = User.query.get(self._user_id)
        data = {
            "id": self.id,
            "title": self._title,
            "content": self._content,
            # "user_name": user.name if user else None,
            # Review information as this may not work as this is a quick workaround
            "post_id": self._post_id
        }
        return data
    
    def temp_update(self):
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
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
        
        title = inputs.get("title", "")
        content = inputs.get("content", "")
        # user_name = inputs.get("user_name", "")
        post_id = inputs.get("post_id", "")
        
        user_id = 1
        
        if title:
            self._title = title
        if content:
            self._content = content
        # if user_id: 
        #     self._user_id = user_id
        if post_id:
            self._post_id = post_id
        
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
        comments = {}
        for comment_data in data:
            _ = comment_data.pop('id', None)  # Remove 'id' from comment_data
            title = comment_data.get("title", None)
            channel = CommentsAndFeedback.query.filter_by(_title=title).first()
            if channel:
                channel.update(comment_data)
            else:
                channel = CommentsAndFeedback(**comment_data)
                channel.create()
        return comments
    

def initComments():
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
        
        # p1 = CommentsAndFeedback(title='Calculus Help', content='Need help with derivatives.', user_id=1, post_id=1)
        # p2 = CommentsAndFeedback(title='Stats Help 2', content='Need help with life.', user_id=1, post_id=2)
        # p3 = CommentsAndFeedback(title='Stats Help', content='Need help with finding proportion.', user_id=1, post_id=2)
        # p4 = CommentsAndFeedback(title='Calculus Help 2', content='I got you bro', user_id=1, post_id=1)
        p1 = CommentsAndFeedback(title='Calculus Help', content='Need help with derivatives.', post_id="73616d706c65706174686e616d65")
        p2 = CommentsAndFeedback(title='Stats Help 2', content='Need help with life.', post_id="73616d706c65706174686e616d66")
        p3 = CommentsAndFeedback(title='Stats Help', content='Need help with finding proportion.', post_id="73616d706c65706174686e616d67")
        p4 = CommentsAndFeedback(title='Calculus Help 2', content='I got you bro', post_id="73616d706c65706174686e616d68")
        
        for comment in [p1, p2, p3, p4]:
            try:
                comment.create()
                print(f"Record created: {repr(comment)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
