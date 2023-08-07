from app.api import bp
from flask import request, jsonify, g, url_for
import time
from app.api.errors import bad_request
from app.model.models import Role,User
import functools
from app.api.errors import bad_request
from app.api.auth import token_auth
from app.api.auth import permission_require
from app import db

@token_auth.verify_token
@bp.route('/roles', methods=['GET'])
@permission_require
def get_roles():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Role.to_collection_dict(Role.query, page, per_page, 'api.get_roles')
    return jsonify(data)

@token_auth.verify_token
@bp.route('/roles/create', methods=['POST'])
@permission_require
def create_role():
    data = request.get_json()
    if not data:
        return '请输入数据'
    message={}
    if 'permission_id' not in data or not data.get('permission_id', None):
        message['permission_id'] = 'Please provide a valid permission_id.'
    if 'permission_name' not in data or not data.get('permission_name', None):
        message['permission_name'] = 'Please provide a valid permission_name.'
    if 'description' not in data or not data.get('description', None):
        message['description'] = 'Please provide a valid description.'
    if message:
        return bad_request(message)
    
    role = Role()
    role.from_dict(data)
    time.asctime(time.localtime())
    role.create_time = time.asctime(time.localtime())
    db.session.add(role)
    db.session.commit()
    response = jsonify(role.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_role', permission_id=role.id)
    return response
    
@token_auth.verify_token
@bp.route('/roles/<int:permission_id>', methods=['GET'])
@permission_require
def get_role(permission_id):
    role = db.session.query(Role).filter(Role.permission_id == permission_id).first()
    if role is None:
        return "NOT FUND",404
    else:
        return jsonify(role.to_dict())

@token_auth.verify_token
@bp.route('/roles/<int:id>', methods=['DELETE'])
@permission_require
def delete_role(id):
    db.session.query(Role).filter(Role.id == id).delete()
    db.session.commit()
    return "success", 200

@token_auth.login_required
@bp.route('/roles/<int:id>/', methods=['POST'])
@permission_require
def update_role(id):
    role = db.session.query(Role).filter(Role.permission_id == id).first()

    if role is None:
        return "NOT FUND",404
    
    data=request.get_json()
    if not data:
        return bad_request('请输入json数据')
    
    message={}
    if 'description' in data and not data.get('description', None):
        message['description'] = 'Please provide a valid description.'

    if 'permisssion_id' in data and not data.get('permisssion_id', None):
        message['permisssion_id'] = 'please provide a valid permisssion_id'
    
    if 'permisssion_name' in data and not data.get('permisssion_name', None):
        message['permisssion_name'] = 'please provide a valid permisssion_name'
    if message:
        return bad_request(message)
    role.from_dict(data,new_role=False)
    db.session.commit()
    return "update success", 200