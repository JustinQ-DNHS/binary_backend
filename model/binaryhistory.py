from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from __init__ import app, db

class BinaryHistory (db.Model):
    """
    BinaryHistory Model
    Represents an event with the year and description associated.
    """
    __tablename__ = 'binaryHistory'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    def __init__(self, year, description):
        """
        Constructor for BinaryHistory.
        """
        self.year = year
        self.description = description

    def __repr__(self):
        """
        Represents the BinaryHistory object as a string for debugging.
        """
        return f"<BinaryHistory(id={self.id}, year='{self.year}', description='{self.description})>"

    def create(self):
        """
        Adds the event to the database and commits the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        Returns the event details as a dictionary.
        """
        return {
            "id": self.id,
            "year": self.year,
            "description": self.description,
        }

    def update(self, data):
        """
        Updates the event with new data and commits the changes.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def delete(self):
        """
        Deletes the event from the database and commits the transaction.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e


def initBinaryHistory():
    """
    Initializes the binaryHistory table and inserts test data for development purposes.
    """
    with app.app_context():
        db.create_all()  # Create the database and tables

        # Sample test data
        events = [
            BinaryHistory(description="Gottfried Wilhelm Leibniz conceives the idea of the binary numeral system in his essay 'Explication de l'Arithmétique Binaire'.", year="1679"),
            BinaryHistory(description="Leibniz formally publishes his work on the binary numeral system in 'Explication de l'Arithmétique Binaire'.", year="1703"),
            BinaryHistory(description="George Boole develops Boolean algebra, which becomes foundational for binary logic.", year="1847"),
            BinaryHistory(description="George Boole publishes 'An Investigation of the Laws of Thought', further detailing Boolean algebra.", year="1854"),
            BinaryHistory(description="Claude Shannon applies Boolean algebra to design electronic circuits in his master's thesis.", year="1937"),
            BinaryHistory(description="John Atanasoff and Clifford Berry create the Atanasoff-Berry Computer (ABC), which uses binary.", year="1939"),
            BinaryHistory(description="John von Neumann outlines the architecture of modern computers, emphasizing binary.", year="1945"),
            BinaryHistory(description="The ENIAC computer is completed, though it uses decimal rather than binary.", year="1946"),
            BinaryHistory(description="Claude Shannon publishes 'A Mathematical Theory of Communication', linking binary to information theory.", year="1948"),
            BinaryHistory(description="Alan Turing's work on binary-based computation contributes to the development of modern computer science.", year="1950"),
            BinaryHistory(description="The UNIVAC I, the first commercial computer, uses binary in its operations.", year="1951"),
            BinaryHistory(description="Binary-coded decimal (BCD) becomes widely adopted for numerical representation in computing.", year="1960"),
            BinaryHistory(description="ASCII (American Standard Code for Information Interchange) is introduced, using binary to represent characters.", year="1964"),
            BinaryHistory(description="The UNIX operating system is created, relying heavily on binary representations.", year="1969"),
            BinaryHistory(description="Intel releases the 4004 microprocessor, the first commercially available processor based on binary.", year="1971"),
            BinaryHistory(description="IBM introduces the PC, making binary-based computing accessible to the public.", year="1980"),
            BinaryHistory(description="The World Wide Web is introduced, built upon binary protocols and systems.", year="1991"),
            BinaryHistory(description="The Y2K problem highlights the importance of binary in year representation and storage.", year="2000"),
            BinaryHistory(description="Bitcoin, based on binary and cryptographic principles, is introduced.", year="2008")
        ]

        # Add each event to the database
        for event in events:
            try:
                db.session.add(event)  # Add the event to the session
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print(f"Record already exists or error occurred: {event}")
