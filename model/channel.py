# channel.py
from sqlite3 import IntegrityError
from sqlalchemy import Text, JSON
from __init__ import app, db
from model.group import Group

class Channel(db.Model):
    """
    Channel Model
    
    The Channel class represents a channel within a group, with customizable attributes.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the channel.
        _name (db.Column): A string representing the name of the channel.
        _attributes (db.Column): A JSON blob representing customizable attributes for the channel.
        _group_id (db.Column): An integer representing the group to which the channel belongs.
    """
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), nullable=False)
    _attributes = db.Column(JSON, nullable=True)
    _group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

    posts = db.relationship('Post', backref='channel', lazy=True)

    def __init__(self, name, group_id, attributes=None):
        """
        Constructor, 1st step in object creation.
        
        Args:
            name (str): The name of the channel.
            group_id (int): The group to which the channel belongs.
            attributes (dict, optional): Customizable attributes for the channel. Defaults to None.
        """
        self._name = name
        self._group_id = group_id
        self._attributes = attributes or {}

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr() built-in function.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Channel(id={self.id}, name={self._name}, group_id={self._group_id}, attributes={self._attributes})"
    
    @property
    def name(self):
        """
        Gets the channel's name.
        
        Returns:
            str: The channel's name.
        """
        return self._name

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
        
        Returns:
            dict: A dictionary containing the channel data.
        """
        return {
            'id': self.id,
            'name': self._name,
            'attributes': self._attributes,
            'group_id': self._group_id
        }
        
    def update(self, inputs):
        """
        Updates the channel object with new data.
        
        Args:
            inputs (dict): A dictionary containing the new data for the channel.
        
        Returns:
            Channel: The updated channel object, or None on error.
        """
        if not isinstance(inputs, dict):
            return self

        name = inputs.get("name", "")
        group_id = inputs.get("group_id", None)

        # Update table with new data
        if name:
            self._name = name
        if group_id:
            self._group_id = group_id

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return self
        
    @staticmethod
    def restore(data):
        channels = {}
        for channel_data in data:
            _ = channel_data.pop('id', None)  # Remove 'id' from channel_data
            name = channel_data.get("name", None)
            channel = Channel.query.filter_by(_name=name).first()
            if channel:
                channel.update(channel_data)
            else:
                channel = Channel(**channel_data)
                channel.create()
        return channels
    
def initChannels():
    """
    The initChannels function creates the Channel table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Channel objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""

        # Home Page Channels
        general = Group.query.filter_by(_name='General').first()
        support = Group.query.filter_by(_name='Support').first()
        home_page_channels = [
            Channel(name='Announcements', group_id=general.id),
            Channel(name='Events', group_id=general.id),
            Channel(name='FAQ', group_id=support.id),
            Channel(name='Help Desk', group_id=support.id)
        ]
        
        # Shared Interest Channels 
        limitless_connection = Group.query.filter_by(_name='Limitless Connections').first() 
        dnhs_football = Group.query.filter_by(_name='DNHS Football').first() 
        school_subjects = Group.query.filter_by(_name='School Subjects').first()
        music = Group.query.filter_by(_name='Music').first()
        satire = Group.query.filter_by(_name='Satire').first()
        activity_hub = Group.query.filter_by(_name='Activity Hub').first()
        shared_interest_channels = [
            Channel(name='Penpal Letters', group_id=limitless_connection.id),
            Channel(name='Game vs Poway', group_id=dnhs_football.id),
            Channel(name='Game vs Westview', group_id=dnhs_football.id),
            Channel(name='Math', group_id=school_subjects.id),
            Channel(name='English', group_id=school_subjects.id),
            Channel(name='Artist', group_id=music.id),
            Channel(name='Music Genre', group_id=music.id),
            Channel(name='Humor', group_id=satire.id),
            Channel(name='Memes', group_id=satire.id),
            Channel(name='Irony', group_id=satire.id),
            Channel(name='Cyber Patriots', group_id=activity_hub.id),
            Channel(name='Robotics', group_id=activity_hub.id),
        ]
        
        #P3 Channels Below
         # Share and Care channels below:
        DNHSCafe = Group.query.filter_by(_name='Study Room').first()
        chess_forum = Group.query.filter_by(_name='Chess Forum').first()
        Underground_Music = Group.query.filter_by(_name='Underground Music').first()
        share_and_care_channels = [
            Channel(name='Math', group_id=DNHSCafe.id),
            Channel(name='Chemistry', group_id=DNHSCafe.id),
            Channel(name='Biology', group_id=DNHSCafe.id),
            Channel(name='English', group_id=DNHSCafe.id),
            Channel(name='Coding', group_id=DNHSCafe.id),
            Channel(name='History', group_id=DNHSCafe.id),
            Channel(name='General', group_id=chess_forum.id),
            Channel(name='Chess Tips', group_id=chess_forum.id),
            Channel(name='Game Updates', group_id=chess_forum.id),
            Channel(name='Artists', group_id=Underground_Music.id),
            Channel(name='Songs', group_id=Underground_Music.id),
            Channel(name='Genres', group_id=Underground_Music.id),
        ]

        # P2 channels below:
        
        # Vote for the GOAT channels below:
        internet_debates = Group.query.filter_by(_name='Internet Debates').first() 
        calico_vote = Group.query.filter_by(_name='Calico Vote').first() 
        dnero_store = Group.query.filter_by(_name='Dnero Store').first()
        beverage_debates = Group.query.filter_by(_name='Beverage Debates').first()
        nfl_goats = Group.query.filter_by(_name='NFL GOATs').first()
        car_debates = Group.query.filter_by(_name='Car Debates').first()
        vote_for_the_goat_channels = [
            Channel(name='Milk vs Cereal', group_id=internet_debates.id),
            Channel(name='Hot Dog Sandwich', group_id=internet_debates.id),
            Channel(name='Pineapple on Pizza', group_id=internet_debates.id),
            Channel(name='Cats vs Dogs', group_id=internet_debates.id),
            Channel(name='Coffee or Tea', group_id=internet_debates.id),
            Channel(name='Economy Cars', group_id=car_debates.id),
            Channel(name='Luxury Cars', group_id=car_debates.id),
            Channel(name='Vintage Cars', group_id=car_debates.id),
            Channel(name='Student Cars', group_id=car_debates.id),
            Channel(name='Adventure Play House', group_id=calico_vote.id),
            Channel(name='Sylvanian Family Restraunt House', group_id=calico_vote.id),
            Channel(name='Magical Mermaid Castle House', group_id=calico_vote.id),
            Channel(name='Woody School House', group_id=calico_vote.id),
            Channel(name='Spooky Suprise Haunted House', group_id=calico_vote.id),
            Channel(name='Brick Oven Bakery House', group_id=calico_vote.id),
            Channel(name='Food and Drink', group_id=dnero_store.id),
            Channel(name='Spirit', group_id=dnero_store.id),
            Channel(name='Limited Edition', group_id=dnero_store.id),
            Channel(name='Quarterbacks', group_id=nfl_goats.id),
            Channel(name='Running Backs', group_id=nfl_goats.id),
            Channel(name='Wide Receivers', group_id=nfl_goats.id),
            Channel(name='Defensive Players', group_id=nfl_goats.id),
            Channel(name='NFL Divisions', group_id=nfl_goats.id),
            Channel(name='Gift Cards', group_id=dnero_store.id),
        ]
        
        # P5 Channels: 
        book_reviews = Group.query.filter_by(_name='Book Reviews').first() 
        instabox = Group.query.filter_by(_name='Instabox').first() 
        flavor_fusion = Group.query.filter_by(_name='Flavor Fusion').first()
        update_the_nest = Group.query.filter_by(_name='Update The Nest').first()
        rate_and_relate_channels = [
            Channel(name='Fiction Books', group_id=book_reviews.id),
            Channel(name='Nonfiction Books', group_id=book_reviews.id),
            Channel(name='Combos', group_id=flavor_fusion.id),
        ]
        
        
        channels = home_page_channels + shared_interest_channels + vote_for_the_goat_channels + rate_and_relate_channels
        for channel in channels:
            try:
                db.session.add(channel)
                db.session.commit()
                print(f"Record created: {repr(channel)}")
            except IntegrityError:
                db.session.rollback()
                print(f"Records exist, duplicate email, or error: {channel.name}")
