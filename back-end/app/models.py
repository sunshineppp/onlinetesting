# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from app import db


class Answer(db.Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    corrent = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.ForeignKey('question.id'), nullable=False)

    question = db.relationship('Question', primaryjoin='Answer.question_id == Question.id', backref='answers')



class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    analysis = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)
    level = db.Column(db.Text, nullable=False)
