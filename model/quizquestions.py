from sqlite3 import IntegrityError
from __init__ import app, db
from model.user import User

class quizquestions(db.Model):
    __tablename__ = 'quizquestions'
    id = db.Column(db.Integer, primary_key=True)
    _q1 = db.Column(db.Integer, nullable=False)
    _q2 = db.Column(db.Integer, nullable=False)
    _q3 = db.Column(db.Integer, nullable=False)
    _q4 = db.Column(db.Integer, nullable=False)
    _q5 = db.Column(db.Integer, nullable=False)
    _q6 = db.Column(db.Integer, nullable=False)
    _q7 = db.Column(db.Integer, nullable=False)
    _q8 = db.Column(db.Integer, nullable=False)
    _q9 = db.Column(db.Integer, nullable=False)
    _q10 = db.Column(db.Integer, nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, user_id):

        self._q1 = q1
        self._q2 = q2
        self._q3 = q3
        self._q4 = q4
        self._q5 = q5
        self._q6 = q6
        self._q7 = q7
        self._q8 = q8
        self._q9 = q9
        self._q10 = q10
        self._user_id = user_id

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(post) built-in function, where post is an instance of the Post class.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Post(id={self.id}, q1={self._q1}, q2={self._q2}, q3={self._q3}, q4={self._q4}, q5={self._q5}, q6={self._q6}, q7={self._q7}, q8={self._q8}, q9={self._q9}, q10={self._q10} user_id={self._user_id})"

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
            "q1": self._q1,
            "q2": self._q2,
            "q3": self._q3,
            "q4": self._q4,
            "q5": self._q5,
            "q6": self._q6,
            "q7": self._q7,
            "q8": self._q8,
            "q9": self._q9,
            "q10": self._q10,
            "user_name": user.name if user else None,
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

def initquizquestions():
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
        
        p1 = quizquestions(q1='0', q2='0', q3='0',q4='0',q5='0',q6='0',q7='0',q8='0',q9='0',q10='0', user_id=1)  
        
        for post in [p1]:
            try:
                post.create()
                print(f"Record created: {repr(post)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {post.uid}")