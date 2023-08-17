# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.model import enums
from werkzeug.security import generate_password_hash, check_password_hash
import time
from datetime import datetime, timedelta
import jwt
from flask import url_for,current_app

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page=page, per_page=per_page)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class Role(PaginatedAPIMixin,db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    permission_id = db.Column(db.Integer, nullable=False, unique=True)
    permission_name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.Text, nullable=False)

    def to_dict(self):
        data = {
            'id': self.id,
            'permission_id': self.permission_id,
            'permission_name': self.permission_name,
            'description': self.description,
            'create_time': self.create_time
            # '_links': {
            # }
        }
        return data


    def from_dict(self, data, new_role = False):
        for field in ['permission_id','permission_name','description']:
            if field in data:
                setattr(self, field, data[field])
        if new_role:
            time_tuple = time.localtime(time.time())
            create_time = "{}年{}月{}日{}点{}分".format(time_tuple[0],time_tuple[1],time_tuple[2],time_tuple[3],time_tuple[4])
            self.create_time = create_time


class User(PaginatedAPIMixin,db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    permission_id = db.Column(db.ForeignKey('role.permission_id', ondelete='CASCADE'), nullable=False)

    role = db.relationship('Role', primaryjoin='User.permission_id == Role.permission_id', backref='user', passive_deletes=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        # return self.password == password
        return check_password_hash(self.password,password)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'account': self.account,
            'permission_id':self.permission_id,
            'email':self.email
            # '_links': {
            #     'self': url_for('api.get_user', id=self.id)
            # }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['account', 'email','permission_id']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            # self.password = data['password']
            self.set_password(data['password'])
        if 'permission_id' not in data:
            self.permission_id = 0
    
    def get_jwt(self, expires_in=6000):
        now = datetime.utcnow()
        payload = {
            'user_id': self.id,
            'account': self.account,
            'permission_id': self.permission_id,
            'exp': now + timedelta(seconds=expires_in),
            'iat': now
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256').encode('utf-8').decode('utf-8')
    
    @staticmethod
    def verify_jwt(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
        except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidSignatureError) as e:
            # Token过期，或被人修改，那么签名验证也会失败
            return '登录过期'
        return User.query.get(payload.get('user_id'))


class Answer(db.Model):
    __tablename__ = 'answer'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    correct = db.Column(db.Integer, nullable = False)
    question_id = db.Column(db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False)

    question = db.relationship('Question', primaryjoin='Answer.question_id == Question.id', backref='answer', passive_deletes = True)



class Question(db.Model):
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    analysis = db.Column(db.Text, nullable=False)
    type = db.Column(db.Enum(enums.QuestionType), nullable=False)
    level = db.Column(db.Enum(enums.QuestionLevel), nullable=False)
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
    question_id = db.Column(db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
    testpaper_id = db.Column(db.ForeignKey('testpaper.id', ondelete='CASCADE'), nullable=False)

    question = db.relationship('Question', primaryjoin='TestpaperQuestion.question_id == Question.id', backref='testpaper_questions', passive_deletes=True)
    testpaper = db.relationship('Testpaper', primaryjoin='TestpaperQuestion.testpaper_id == Testpaper.id', backref='testpaper_questions', passive_deletes=True)


class UserExam(db.Model):
    __tablename__ = 'user_exam'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    testpaper_id = db.Column(db.ForeignKey('testpaper.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
    answer = db.Column(db.Text, nullable=True)
    correct = db.Column(db.Boolean, nullable=True)
    score = db.Column(db.Float, nullable=True)
    exam_time = db.Column(db.Text, nullable=True)

    user = db.relationship('User', primaryjoin='UserExam.user_id == User.id', backref='user_exam', passive_deletes=True)
    question = db.relationship('Question', primaryjoin='UserExam.question_id == Question.id', backref='user_exam', passive_deletes=True)
    testpaper = db.relationship('Testpaper', primaryjoin='UserExam.testpaper_id == Testpaper.id', backref='user_exam', passive_deletes=True)

    # def to_dict(self):
    #     data = {
    #         'permission_id': self.permission_id,
    #         'permission_name': self.permission_name,
    #         'description': self.description,
    #         'create_time': self.create_time
    #         # '_links': {
    #         # }
    #         }
    #     return data


    def from_dict(self, data):
        for field in ['question_id','answer',]:
            if field in data:
                setattr(self, field, data[field])

    def to_dict(self):
        data = {
            "user_id":self.user_id,
            "tespaper_id":self.testpaper_id,
            "question_id":self.question_id,
            "answer":self.answer,
            "correct":self.correct,
            "score":self.score,
            "exam_time":self.exam_time,
        }
        return data
    
