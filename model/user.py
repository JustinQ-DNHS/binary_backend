# user.py
from flask import current_app
from flask_login import UserMixin
from datetime import date
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

from __init__ import app, db

""" Helper Functions """

def default_year():
    """
    Returns the default year for user enrollment based on the current month.
    
    If the current month is between August (8) and December (12), the enrollment year is the next year.
    Otherwise, it is the current year.
    
    Returns:
        int: The default year for user enrollment.
    """
    current_month = date.today().month
    current_year = date.today().year
    if 7 <= current_month <= 12:
        current_year += 1
    return current_year 

""" Database Models """

''' Tutorial: https://www.sqlalchemy.org/library.html#tutorials, try to get into Python shell and follow along '''

class User(db.Model, UserMixin):
    """
    User Model

    This class represents the User model, which is used to manage actions in the 'users' table of the database. It is an
    implementation of Object Relational Mapping (ORM) using SQLAlchemy, allowing for easy interaction with the database
    using Python code. The User model includes various fields and methods to support user management, authentication,
    and profile management functionalities.

    Attributes:
        __tablename__ (str): Specifies the name of the table in the database.
        id (Column): The primary key, an integer representing the unique identifier for the user.
        _name (Column): A string representing the user's name. It is not unique and cannot be null.
        _uid (Column): A unique string identifier for the user, cannot be null.
        _password (Column): A string representing the hashed password of the user. It is not unique and cannot be null.
        _role (Column): A string representing the user's role within the application. Defaults to "User".
        _pfp (Column): A string representing the path to the user's profile picture. It can be null.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _email = db.Column(db.String(255), unique=False, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _role = db.Column(db.String(20), default="User", nullable=False)
    _pfp = db.Column(db.String(255), unique=False, nullable=True)
    _car = db.Column(db.String(255), unique=False, nullable=True)
   
    posts = db.relationship('Post', backref='author', lazy=True)
                                 
    
    def __init__(self, name, uid, password="", role="User", pfp='', car='', email='?'):
        """
        Constructor, 1st step in object creation.
        
        Args:
            name (str): The name of the user.
            uid (str): The unique identifier for the user.
            password (str): The password for the user.
            role (str): The role of the user within the application. Defaults to "User".
            pfp (str): The path to the user's profile picture. Defaults to an empty string.
        """
        self._name = name
        self._uid = uid
        self._email = email
        self.set_password(password)
        self._role = role
        self._pfp = pfp
        self._car = car

    # UserMixin/Flask-Login requires a get_id method to return the id as a string
    def get_id(self):
        """
        Returns the user's ID as a string.
        
        Returns:
            str: The user's ID.
        """
        return str(self.id)

    # UserMixin/Flask-Login requires is_authenticated to be defined
    @property
    def is_authenticated(self):
        """
        Indicates whether the user is authenticated.
        
        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        return True

    # UserMixin/Flask-Login requires is_active to be defined
    @property
    def is_active(self):
        """
        Indicates whether the user is active.
        
        Returns:
            bool: True if the user is active, False otherwise.
        """
        return True

    # UserMixin/Flask-Login requires is_anonymous to be defined
    @property
    def is_anonymous(self):
        """
        Indicates whether the user is anonymous.
        
        Returns:
            bool: True if the user is anonymous, False otherwise.
        """
        return False
    
    @property
    def email(self):
        """
        Gets the user's email.
        
        Returns:
            str: The user's email.
        """
        return self._email
    
    @email.setter
    def email(self, email):
        """
        Sets the user's email.
        
        Args:
            email (str): The new email for the user.
        """
        if email is None or email == "":
            self._email = "?"
        else:
            self._email = email
        
    def set_email(self):
        """
        Sets the email of the user based on the UID 
        """
        self.email = "?"

    @property
    def name(self):
        """
        Gets the user's name.
        
        Returns:
            str: The user's name.
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the user's name.
        
        Args:
            name (str): The new name for the user.
        """
        self._name = name

    @property
    def uid(self):
        """
        Gets the user's unique identifier.
        
        Returns:
            str: The user's unique identifier.
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """
        Sets the user's unique identifier.
        
        Args:
            uid (str): The new unique identifier for the user.
        """
        self._uid = uid

    def is_uid(self, uid):
        """
        Checks if the provided UID matches the user's UID.
        
        Args:
            uid (str): The UID to check.
        
        Returns:
            bool: True if the UID matches, False otherwise.
        """
        return self._uid == uid

    @property
    def password(self):
        """
        Gets the user's password (partially obscured for security).
        
        Returns:
            str: The user's password (first 10 characters followed by "...").
        """
        return self._password[0:10] + "..."  # because of security only show 1st characters

    def set_password(self, password):
        """
        Sets the user's password (hashed).
        
        Args:
            password (str): The new password for the user.
        """
        if not password or password == "":
            password=app.config["DEFAULT_PASSWORD"]
        self._password = generate_password_hash(password, "pbkdf2:sha256", salt_length=10)

    def is_password(self, password):
        """
        Checks if the provided password matches the user's stored password.
        
        Args:
            password (str): The password to check.
        
        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self._password, password)

    def __str__(self):
        """
        Returns a string representation of the user object (JSON format).
        
        Returns:
            str: A JSON string representation of the user object.
        """
        return json.dumps(self.read())

    @property
    def role(self):
        """
        Gets the user's role.
        
        Returns:
            str: The user's role.
        """
        return self._role

    @role.setter
    def role(self, role):
        """
        Sets the user's role.
        
        Args:
            role (str): The new role for the user.
        """
        self._role = role

    def is_admin(self):
        """
        Checks if the user is an admin.
        
        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        return self._role == "Admin"
    
    @property
    def pfp(self):
        """
        Gets the user's profile picture path.
        
        Returns:
            str: The path to the user's profile picture.
        """
        return self._pfp

    @pfp.setter
    def pfp(self, pfp):
        """
        Sets the user's profile picture path.
        
        Args:
            pfp (str): The new profile picture path for the user.
        """
        self._pfp = pfp

    @property
    def car(self):
        return self._car
    @car.setter
    def car(self, car):
        self._car = car
    def create(self, inputs=None):
        """
        Adds a new record to the table and commits the transaction.
        
        Args:
            inputs (dict, optional): Additional data to update the user with.
        
        Returns:
            User: The created user object, or None on error.
        """
        try:
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            if inputs:
                self.update(inputs)
            return self
        except IntegrityError:
            db.session.rollback()
            return None

    def read(self):
        """
        Converts the user object to a dictionary.
        
        Returns:
            dict: A dictionary representation of the user object.
        """
        data = {
            "id": self.id,
            "uid": self.uid,
            "name": self.name,
            "email": self.email,
            "role": self._role,
            "pfp": self._pfp,
            "car": self._car
        }
        return data
        
    def update(self, inputs):
        """
        Updates the user object with new data.
        
        Args:
            inputs (dict): A dictionary containing the new data for the user.
        
        Returns:
            User: The updated user object, or None on error.
        """
        if not isinstance(inputs, dict):
            return self

        name = inputs.get("name", "")
        uid = inputs.get("uid", "")
        password = inputs.get("password", "")
        pfp = inputs.get("pfp", None)

        # Update table with new data
        if name:
            self.name = name
        if uid:
            self.set_uid(uid)
        if password:
            self.set_password(password)
        if pfp is not None:
            self.pfp = pfp

        # Check this on each update
        self.set_email()

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return self
    
    def delete(self):
        """
        Removes the user object from the database and commits the transaction.
        
        Returns:
            None
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return None   
    
    def save_pfp(self, image_data, filename):
        """
        Saves the user's profile picture.
        
        Args:
            image_data (bytes): The image data of the profile picture.
            filename (str): The filename of the profile picture.
        """
        try:
            user_dir = os.path.join(app.config['UPLOAD_FOLDER'], self.uid)
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
            file_path = os.path.join(user_dir, filename)
            with open(file_path, 'wb') as img_file:
                img_file.write(image_data)
            self.update({"pfp": filename})
        except Exception as e:
            raise e
        
    def delete_pfp(self):
        """
        Deletes the user's profile picture from the user record.
        """
        self.pfp = None
        db.session.commit()
        
    def save_car(self, image_data, filename):
        """
        Saves the user's car picture.
        
        Args:
            image_data (bytes): The image data of the car picture.
            filename (str): The filename of the car picture.
        """
        try:
            user_dir = os.path.join(app.config['UPLOAD_FOLDER'], self.uid)
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
            file_path = os.path.join(user_dir, filename)
            with open(file_path, 'wb') as img_file:
                img_file.write(image_data)
            self.update({"car": filename})
        except Exception as e:
            raise e
        
    def delete_car(self):
        """
        Deletes the user's profile picture from the user record.
        """
        self.car = None
        db.session.commit()
        
    def set_uid(self, new_uid=None):
        """
        Updates the user's directory based on the new UID provided.

        Args:
            new_uid (str, optional): The new UID to update the user's directory.
        
        Returns:
            User: The updated user object.
        """
        # Store the old UID for later comparison
        old_uid = self._uid
        # Update the UID if a new one is provided
        if new_uid and new_uid != self._uid:
            self._uid = new_uid
            # Commit the UID change to the database
            db.session.commit()

        # If the UID has changed, update the directory name
        if old_uid != self._uid:
            old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], old_uid)
            new_path = os.path.join(current_app.config['UPLOAD_FOLDER'], self._uid)
            if os.path.exists(old_path):
                os.rename(old_path, new_path)
                
    @staticmethod
    def restore(data):
        users = {}
        for user_data in data:
            _ = user_data.pop('id', None)  # Remove 'id' from user_data and store it in user_id
            uid = user_data.get("uid", None)
            user = User.query.filter_by(_uid=uid).first()
            if user:
                user.update(user_data)
            else:
                user = User(**user_data)
                user.create()
        return users


"""Database Creation and Testing """

def initUsers():
    """
    The initUsers function creates the User table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        User objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        
        u1 = User(name='Thomas Edison', uid=app.config['ADMIN_USER'], password=app.config['ADMIN_PASSWORD'], pfp='toby.png', car='toby_car.png', role="Admin")
        u2 = User(name='Grace Hopper', uid=app.config['DEFAULT_USER'], password=app.config['DEFAULT_PASSWORD'], pfp='hop.png')
        u3 = User(name='Nicholas Tesla', uid='niko', password='123niko', pfp='niko.png' )
        users = [u1, u2, u3]
        
        for user in users:
            try:
                user.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
