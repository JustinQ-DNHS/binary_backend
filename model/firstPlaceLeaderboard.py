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
    _time_in_first_place = db.Column(db.Integer, nullable=False)
    _games_played = db.Column(db.Integer, nullable=False)  
    _average_score = db.Column(db.Integer, nullable=False)  # New attribute
    _wins = db.Column(db.Integer, nullable=False)  # New attribute
    _losses = db.Column(db.Integer, nullable=False) # New attribute
    _last_played = db.Column(db.DateTime, nullable=True)  # New attribute
    _highest_score = db.Column(db.Integer, nullable=False)  # New attribute

    def __init__(self, username, user_id, time_in_first_place, games_played, average_score, wins, losses, last_played, highest_score):
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
        self._time_in_first_place = time_in_first_place
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
        return f"BinaryScore(id={self.id}, username={self._username}, user_id={self._user_id}, user_time_in_first_place={self._time_in_first_place}, user_games_played={self._games_played}, average_score={self._average_score}, wins={self._wins}, losses={self._losses}, last_played={self._last_played}, highest_score={self._highest_score})"

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
            "user_time_in_first_place": self._time_in_first_place,
            "user_games_played": self._games_played,
            "average_score": self._average_score,
            "wins": self._wins,
            "losses": self._losses,
            "last_played": self._last_played,
            "highest_score": self._highest_score
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
        
    @staticmethod
    def restore(data):
        restored_time = {}
        for firstPLaceLeaderboard_data in data:
            time = firstPlaceLeaderboard(firstPLaceLeaderboard_data['username'], firstPLaceLeaderboard_data['user_id'], firstPLaceLeaderboard_data['time_in_first_place'], firstPLaceLeaderboard_data['games_played'], firstPLaceLeaderboard_data['average_score'], firstPLaceLeaderboard_data['wins'], firstPLaceLeaderboard_data['losses'], firstPLaceLeaderboard_data['last_played'], firstPLaceLeaderboard_data['highest_score'])
            time.create()
            restored_time[time.id] = time
        return restored_time
        

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
        
        p1 = firstPlaceLeaderboard(username="JIM", user_id="jim_is_the_best", time_in_first_place="10", games_played="5", average_score="5.0", wins="3", losses="2", last_played=datetime.datetime.now(), highest_score="10")
        p2 = firstPlaceLeaderboard(username="TIM", user_id="tim_10", time_in_first_place="2", games_played="3", average_score="3.0", wins="2", losses="1", last_played=datetime.datetime.now(), highest_score="5")
        p3 = firstPlaceLeaderboard(username="BUM", user_id="dum_bum", time_in_first_place="7", games_played="7", average_score="4.0", wins="4", losses="3", last_played=datetime.datetime.now(), highest_score="7")
        p4 = firstPlaceLeaderboard(username="TUM", user_id="tum123", time_in_first_place="5", games_played="4", average_score="4.5", wins="3", losses="1", last_played=datetime.datetime.now(), highest_score="8")
        
        for post in [p1, p2, p3, p4]:
            try:
                post.create()
                print(f"Record created: {repr(post)}")
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {post.user_id}")