from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from __init__ import db

class lgate(db.Model):
    __tablename__ = 'lgate'  # Explicit table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    quiz_id = db.Column(db.Integer, nullable=False)

    def __init__(self, name, score, quiz_id):
        self.name = name
        self.score = score
        self.quiz_id = quiz_id

    def read(self):
        return {
            'id': self.id,
            'name': self.name,
            'score': self.score,
            'quiz_id': self.quiz_id
        }
    def __repr__(self):
        """
        Represents the lgate object as a string for debugging.
        """
        return f"<lgate(id={self.id}, name='{self.name}', score='{self.score}', quiz_id={self.quiz_id})>"

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
            "name": self.name,
            "score": self.score,
            "quiz_id": self.quiz_id
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


def initlgate():
    """
    Initializes the lgate table and inserts test data for development purposes.
    """
    with app.app_context():
        db.create_all()  # Create the database and tables

        # Sample test data
        lgate = [
            lgate(name="Jake", score="3", quiz_id=1),
            lgate(name="Josh", score="4", quiz_id=2),
            lgate(name="Julia", score="5", quiz_id=3)
        ]

        for quiz in lgate:
            try:
                quiz.create()
                print(f"Created quiz: {quiz}")
            except IntegrityError:
                db.session.rollback()
                print(f"Record already exists or error occurred: {quiz}")
