from app.api import bp
from flask import request, jsonify, url_for
from app import db
from app.api.errors import bad_request
from app.model.models import User
from app.api.auth import token_auth,permission_require
import re


def create_user():
    data = request.get_json()
    if not data:
        return '请输入数据'
    
    message={}
    if 'account' not in data or not data.get('account', None):
        message['account'] = 'Please provide a valid username.'
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, data.get('email', None)):
        message['email'] = 'Please provide a valid email address.'
    if 'password' not in data or not data.get('password', None):
        message['password'] = 'Please provide a valid password.'

    if User.query.filter_by(account=data.get('account', None)).first():
        message['account'] = 'Please use a different account.'
    if User.query.filter_by(email=data.get('email', None)).first():
        message['email'] = 'Please use a different email address.'
    
    if request.headers.get('Authorization') is not None:
        if 'permission_id' not in data or not data.get('permission_id', None):
            message['permission_id'] = 'Please provide a valid permission_id.'
    else:
        if 'permission_id' in data:
            data.pop('permission_id')
            message['permission_id'] = 'No permission'
    
    if message:
        return bad_request(message)

    user = User()
    user.from_dict(data,new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users/create',methods=['POST'])
def user_create_user():
    return create_user()

@token_auth.login_required
@bp.route('/users/adminCreate',methods=['POST'])
@permission_require
def admin_create_user():
    return create_user()

@token_auth.login_required
@bp.route('/users/', methods=['GET'])
@permission_require
def get_users():
    # page = request.args.get('page', 1, type=int)
    # per_page = min(request.args.get('per_page', 10, type=int), 100)
    # data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    resources =  db.session.query(User).all()
    data = {
        'users': [item.to_dict() for item in resources]
    }
    return jsonify(data)

@token_auth.login_required
@bp.route('/users/<int:id>/', methods=['GET'])
@permission_require
def get_user(id):
    return jsonify(db.session.query(User).get_or_404(id).to_dict())

@token_auth.login_required
@bp.route('/users/<int:id>/', methods=['POST'])
@permission_require
def update_user(id):
    user = db.session.query(User).get_or_404(id)
    data=request.get_json()
    if not data:
        return bad_request('请输入json数据')
    message={}

    if 'account' in data and not data.get('account', None):
        message['account'] = 'Please provide a valid account.'

    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' in data and not re.match(pattern, data.get('email', None)):
        message['email'] = 'Please provide a valid email address.'

    if 'account' in data and data['account'] != user.account and \
            User.query.filter_by(account=data['account']).first():
        message['account'] = 'Please use a different username.'
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        message['email'] = 'Please use a different email address.'
    if 'permisssion_id' in data and not data.get('permisssion_id', None):
        message['permisssion_id'] = 'please provide a valid permisssion_id'

    if message:
        return bad_request(message)

    user.from_dict(data,new_user=False)
    # interface/thunder-collection_user.json
    db.session.commit()
    return "update success", 200

@token_auth.login_required
@bp.route('/users/<int:id>',methods=['DELETE'])
@permission_require
def delete_user(id):
    db.session.query(User).filter(User.id == id).delete()
    # user = db.session.query(User).filter(User.id == id).first()
    # db.session.delete(user)
    db.session.commit()
    return "delete success", 200


