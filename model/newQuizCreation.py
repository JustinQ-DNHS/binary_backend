from sqlite3 import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from __init__ import app, db

class QuizCreation(db.Model):
    """
    QuizCreation Model
    
    Represents a quiz with a question, answer, and a quiz_id associated with a user.
    """
    __tablename__ = 'quizCreation'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    quiz_id = db.Column(db.Integer, nullable=False)  # Remove ForeignKey for simplicity in SQLite

    def __init__(self, question, answer, quiz_id):
        """
        Constructor for QuizCreation.
        """
        self.question = question
        self.answer = answer
        self.quiz_id = quiz_id

    def __repr__(self):
        """
        Represents the QuizCreation object as a string for debugging.
        """
        return f"<QuizCreation(id={self.id}, question='{self.question}', answer='{self.answer}', quiz_id={self.quiz_id})>"

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
            "question": self.question,
            "answer": self.answer,
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


def initQuizCreation():
    """
    Initializes the QuizCreation table and inserts test data for development purposes.
    """
    with app.app_context():
        db.create_all()  # Create the database and tables

        # Sample test data
        quizzes = [
            QuizCreation(question="What is the capital of France?", answer="Paris", quiz_id=1),
            QuizCreation(question="What is 2 + 2?", answer="4", quiz_id=2),
            QuizCreation(question="Who wrote 'To Kill a Mockingbird'?", answer="Harper Lee", quiz_id=3)
        ]

        for quiz in quizzes:
            try:
                quiz.create()
                print(f"Created quiz: {quiz}")
            except IntegrityError:
                db.session.rollback()
                print(f"Record already exists or error occurred: {quiz}")
