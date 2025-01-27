# post.py
from sqlite3 import IntegrityError
from sqlalchemy import Text
import datetime
from __init__ import app, db
from model.user import User

class firstPlaceLeaderboard(db.Model):
    """
    Binary Learning Game Scores Model
    
    The class represents an individual contribution or discussion within a group.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the post.
    """
    __tablename__ = 'firstPlaceLeaderboard'

    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column(db.String(255), nullable=False)
    _user_id = db.Column(db.String(255), db.ForeignKey('users.id'), nullable=False)
    _games_played = db.Column(db.Integer, nullable=False)  
    _average_score = db.Column(db.Integer, nullable=False) 
    _wins = db.Column(db.Integer, nullable=False)  
    _losses = db.Column(db.Integer, nullable=False) 
    _last_played = db.Column(db.DateTime, nullable=True)  
    _highest_score = db.Column(db.Integer, nullable=False)  

    def __init__(self, username, user_id, games_played, average_score, wins, losses, last_played, highest_score):
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
        self._games_played = games_played
        self._average_score = average_score
        self._wins = wins
        self._losses = losses
        self._last_played = last_played
        self._highest_score = highest_score

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr(post) built-in function, where post is an instance of the Post class.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"BinaryScore(id={self.id}, username={self._username}, user_id={self._user_id}, user_games_played={self._games_played}, average_score={self._average_score}, wins={self._wins}, losses={self._losses}, last_played={self._last_played}, highest_score={self._highest_score})"

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
            "user_games_played": self._games_played,
            "average_score": self._average_score,
            "wins": self._wins,
            "losses": self._losses,
            "last_played": self._last_played,
            "highest_score": self._highest_score
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
        
        games_played = inputs.get('games_played')
        average_score = inputs.get('average_score')
        wins = inputs.get('wins')
        losses = inputs.get('losses')
        last_played = inputs.get('last_played')
        highest_score = inputs.get('highest_score')

        if (games_played):
            self._games_played = games_played
        if (average_score):
            self._average_score = average_score
        if (wins):
            self._wins = wins
        if (losses):
            self._losses = losses
        if (last_played):
            self._last_played = last_played
        if (highest_score):
            self._highest_score = highest_score

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
        existing_sections = {section._username: section for section in firstPlaceLeaderboard.query.all()}
        for section_data in data:
            _ = section_data.pop('id', None)
            username = section_data.get("username", None)
            section = existing_sections.pop(username, None)
            if section:
                section.update(section_data)
            else:
                section = firstPlaceLeaderboard(**section_data)
                section.create()
            
        for section in existing_sections.values():
            db.session.delete(section)
        
        db.session.commit()
        return sections
        

def initFirstPlaceLeaderboard():
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
        
        p1 = firstPlaceLeaderboard(username="JIM", user_id="jim_is_the_best", games_played="5", average_score="5.0", wins="3", losses="2", last_played=datetime.datetime.now(), highest_score="10")
        p2 = firstPlaceLeaderboard(username="TIM", user_id="tim_10", games_played="3", average_score="3.0", wins="2", losses="1", last_played=datetime.datetime.now(), highest_score="5")
        p3 = firstPlaceLeaderboard(username="BUM", user_id="dum_bum", games_played="7", average_score="4.0", wins="4", losses="3", last_played=datetime.datetime.now(), highest_score="7")
        p4 = firstPlaceLeaderboard(username="TUM", user_id="tum123", games_played="4", average_score="4.5", wins="3", losses="1", last_played=datetime.datetime.now(), highest_score="8")
        
        for post in [p1, p2, p3, p4]:
            try:
                post.create()
                print(f"Record created: {repr(post)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {post.user_id}")