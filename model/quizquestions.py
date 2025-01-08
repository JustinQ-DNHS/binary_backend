from sqlite3 import IntegrityError
from __init__ import app, db
from model.user import User

class quizquestions(db.Model):
    __tablename__ = 'quizquestions'

    id = db.Column(db.Integer, primary_key=True)
    _q1 = db.Column(db.Integer, nullable=False)
    _q2 = db.Column(db.Integer, nullable=False)
    _q3 = db.Column(db.Integer, nullable=False)
    _q4 = db.Column(db.Integer, nullable=False)
    _q5 = db.Column(db.Integer, nullable=False)
    _q6 = db.Column(db.Integer, nullable=False)
    _q7 = db.Column(db.Integer, nullable=False)
    _q8 = db.Column(db.Integer, nullable=False)
    _q9 = db.Column(db.Integer, nullable=False)
    _q10 = db.Column(db.Integer, nullable=False)
    _user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)