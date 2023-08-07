# coding: utf-8
from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import time
from datetime import datetime, timedelta
import jwt
from flask import url_for,current_app

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page=1, per_page=10)
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


class User(PaginatedAPIMixin,db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    permission_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        # return self.password == password
        return check_password_hash(self.password,password)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'account': self.account,
            'permission_id':self.permission_id
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
            self.permission_id = 0
            # self.password = data['password']
            self.set_password(data['password'])
    
    def get_jwt(self, expires_in=600):
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
            return None
        return User.query.get(payload.get('user_id'))




class Role(PaginatedAPIMixin,db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    permission_id = db.Column(db.ForeignKey('user.permission_id'), nullable=False)
    permission_name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.Text, nullable=False)

    permission = db.relationship('User', primaryjoin='Role.permission_id == User.permission_id', backref='roles')

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
            create_time = "当前时间为{}年{}月{}日{}点{}分{}秒".format(time_tuple[0],time_tuple[1],time_tuple[2],time_tuple[3],time_tuple[4],time_tuple[5])
            self.create_time = create_time
