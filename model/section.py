# section.py
from sqlite3 import IntegrityError
from __init__ import app, db

class Section(db.Model):
    """
    Section Model
    
    The Section class represents a broad area of interest.
    
    Attributes:
        id (db.Column): The primary key, an integer representing the unique identifier for the section.
        _name (db.Column): A string representing the name of the section.
        _theme (db.Column): A string representing the theme of the section.
    """
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=True, nullable=False)
    _theme = db.Column(db.String(255), nullable=True)

    groups = db.relationship('Group', backref='section', lazy=True)

    def __init__(self, name, theme=None):
        """
        Constructor, 1st step in object creation.
        
        Args:
            name (str): The name of the section.
            theme (str, optional): The theme of the section. Defaults to None.
        """
        self._name = name
        self._theme = theme

    def __repr__(self):
        """
        The __repr__ method is a special method used to represent the object in a string format.
        Called by the repr() built-in function.
        
        Returns:
            str: A text representation of how to create the object.
        """
        return f"Section(id={self.id}, name={self._name}, theme={self._theme})"

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
            dict: A dictionary containing the section data.
        """
        return {
            'id': self.id,
            'name': self._name,
            'theme': self._theme
        }
        
    def update(self, inputs):
        """
        Updates the section object with new data.
        
        Args:
            inputs (dict): A dictionary containing the new data for the section.
        
        Returns:
            Section: The updated section object, or None on error.
        """
        if not isinstance(inputs, dict):
            return self

        name = inputs.get("name", "")
        theme = inputs.get("theme", "")

        # Update table with new data
        if name:
            self._name = name
        if theme:
            self._theme = theme

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return self
    
    @staticmethod
    def restore(data):
        sections = {}
        for section_data in data:
            _ = section_data.pop('id', None)  # Remove 'id' from section_data
            name = section_data.get("name", None)
            section = Section.query.filter_by(_name=name).first()
            if section:
                section.update(section_data)
            else:
                section = Section(**section_data)
                section.create()        
        db.session.commit()
        return sections

def initSections():
    """
    The initSections function creates the Section table and adds tester data to the table.
    
    Uses:
        The db ORM methods to create the table.
    
    Instantiates:
        Section objects with tester data.
    
    Raises:
        IntegrityError: An error occurred when adding the tester data to the table.
    """
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
       
        s1 = Section(name='Home Page') 
        s2 = Section(name='Shared Interest')
        s3 = Section(name='Create and Compete')
        s4 = Section(name='Vote for the GOAT')
        s5 = Section(name='Share and Care')
        s6 = Section(name='Rate and Relate')
        sections = [s1, s2, s3, s4, s5, s6]
        
        for section in sections:
            try:
                section.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.remove()
                print(f"Records exist, duplicate email, or error: {section._name}")