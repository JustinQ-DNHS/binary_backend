from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from __init__ import app, db

class BinaryConverter (db.Model):
    """
    BinaryConverter Model
    
    Represents a quiz with a question and answer associated with a user.
    """
    __tablename__ = 'binaryConverter'

    id = db.Column(db.Integer, primary_key=True)
    binary = db.Column(db.String(255), nullable=False)
    decimal = db.Column(db.String(255), nullable=False)
     

    def __init__(self, binary, decimal, ):
        """
        Constructor for Binary.
        """
        self.binary = binary
        self.decimal = decimal
        

    def __repr__(self):
        """
        Represents the QuizCreation object as a string for debugging.
        """
        return f"<QuizCreation(id={self.id}, question='{self.binary}', answer='{self.decimal})>"

    def create(self):
        """
        Adds the quiz to the database and commits the transaction.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        Returns the quiz details as a dictionary.
        """
        return {
            "id": self.id,
            "binary": self.binary,
            "decimal": self.decimal,
        }

    def update(self, data):
        """
        Updates the quiz with new data and commits the changes.
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
        Deletes the quiz from the database and commits the transaction.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

    @staticmethod
    def restore(data):
        existing_sections = {section.id: section for section in BinaryConverter.query.all()}
        for section_data in data:
            _ = section_data.pop('id', None)  # Remove 'id' from section_data
            binary = section_data.get("binary", None)
            section = existing_sections.pop(binary, None)
            if section:
                section.update(section_data)
            else:
                section = BinaryConverter(**section_data)
                section.create()
        
        # Remove any extra data that is not in the backup
        for section in existing_sections.values():
            db.session.delete(section)
        
        db.session.commit()
        return existing_sections

def initBinaryConverter():
    """
    Initializes the QuizCreation table and inserts test data for development purposes.
    """
    with app.app_context():
        db.create_all()  # Create the database and tables

        # Sample test data
        quizzes = [
            BinaryConverter(decimal="7777", binary="1111001100001"),
            BinaryConverter(decimal="2323", binary="100100010011"),
            
        ]

        for quiz in quizzes:
            try:
                quiz.create()
                print(f"Created quiz: {quiz}")
            except IntegrityError:
                db.session.rollback()
                print(f"Record already exists or error occurred: {quiz}")
