# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from app import db


class Answer(db.Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    correct = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.ForeignKey('question.id'), nullable=False)

    question = db.relationship('Question', primaryjoin='Answer.question_id == Question.id', backref='answers')



class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    analysis = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)
    level = db.Column(db.Text, nullable=False)
    point = db.Column(db.Float, nullable=False)



class Testpaper(db.Model):
    __tablename__ = 'testpaper'

    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    passline = db.Column(db.Float, nullable=False)
    created = db.Column(db.Text, nullable=False)



class TestpaperQuestion(db.Model):
    __tablename__ = 'testpaper_question'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.ForeignKey('question.id'), nullable=False)
    testpaper_id = db.Column(db.ForeignKey('testpaper.id'), nullable=False)

    question = db.relationship('Question', primaryjoin='TestpaperQuestion.question_id == Question.id', backref='testpaper_questions')
    testpaper = db.relationship('Testpaper', primaryjoin='TestpaperQuestion.testpaper_id == Testpaper.id', backref='testpaper_questions')
