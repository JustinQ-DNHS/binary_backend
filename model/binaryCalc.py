from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from model.user import User


class binaryCalc(db.Model):
    __tablename__ = 'binaryCalcValue'


    id = db.Column(db.Integer, primary_key=True)
    _user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    _decimal_value = db.Column(db.Integer, nullable=False)


    def __init__(self, user_id, binary_value, decimal_value):
       """
       Constructor, 1st step in object creation.
      
       Args:
           title (str): The title of the post.
           content (str): The content of the post.
           user_id (int): The user who created the post.
           group_id (int): The group to which the post belongs.
           image_url (str): The url path to the image
       """
       self._user_id = user_id
       self._decimal_value = decimal_value


    def __repr__(self):
       """
       The __repr__ method is a special method used to represent the object in a string format.
       Called by the repr(post) built-in function, where post is an instance of the Post class.
      
       Returns:
           str: A text representation of how to create the object.
       """
       return f"Binary(id={self.id},user_id={self._user_id}, binary_value={self._binary_value})"


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
           "user_id": self._user_id if user else None,
           "decimal_value": self._decimal_value
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
       
def initBinaryCalc():
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
        
        p1 = binaryCalc(user_id="1", decimal_value=1)
        p2 = binaryCalc(user_id="2", decimal_value=3)
        p3 = binaryCalc(user_id="3", decimal_value=7)
        p4 = binaryCalc(user_id="4", decimal_value=15)
        
        for post in [p1, p2, p3, p4]:
            try:
                post.create()
                print(f"Record created: {repr(post)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {post.user_id}")
