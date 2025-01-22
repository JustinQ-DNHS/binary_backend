from sqlite3 import IntegrityError
from sqlalchemy import Text
from __init__ import app, db
from model.user import User

class quizquestions(db.Model):
    __tablename__ = 'quizquestions'
    
    id = db.Column(db.Integer, primary_key=True)
    _question = db.Column(db.String(255), nullable=False)

    
    def __init__(self, question):
       self._question = question



    def __repr__(self):
       """
       The __repr__ method is a special method used to represent the object in a string format.
       Called by the repr(post) built-in function, where post is an instance of the Post class.
      
       Returns:
           str: A text representation of how to create the object.
       """
       return f"Post(id={self.id}, q1={self._question})"


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
           "q1": self._question,

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
      
       p1 = quizquestions(question="What is the capital of France?") 
       p2 = quizquestions(question="What is the capital of Britain?") 
       p3 = quizquestions(question="What is the capital of China?") 
       p4 = quizquestions(question="What is the capital of India?") 
       p5 = quizquestions(question="What is the capital of Japan?") 
      
       for question in [p1, p2, p3, p4, p5]:
           try:
               question.create()
               print(f"Record created: {repr(question)}")
           except IntegrityError:
               '''fails with bad or duplicate data'''
               db.session.remove()

