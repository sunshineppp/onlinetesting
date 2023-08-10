from flask import g, request,current_app
from flask_httpauth import HTTPBasicAuth,HTTPTokenAuth
from app.model.models import User
from app.api.errors import error_response,bad_request
import functools
import jwt


basic_auth = HTTPBasicAuth(scheme='custom')
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(account, password):
    '''用于检查用户提供的用户名和密码'''
    user = User.query.filter_by(account=account).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


@basic_auth.error_handler
def basic_auth_error():
    '''用于在认证失败的情况下返回错误响应'''
    return error_response(401)

def permission_require(func):
    @functools.wraps(func)
    def inner(**kwargs):
        # 获取权限
        token = request.headers.get('Authorization')
        try:
            payload = jwt.decode(
                    token,
                    current_app.config['SECRET_KEY'],
                    algorithms=['HS256'])
        except (jwt.exceptions.ExpiredSignatureError):
            return bad_request('notfun')
        permission = payload.get('permission_id')
        # permission = data['login_permission_id']
        # # 如果权限不够 返回错误信息
        # print(permission)
        if permission == 3:
            # print(111111111111)
            return func(**kwargs)
        else:
            message={}
            message['login_permission_require'] = 'NO PERMISSION'
            # print(22222222222222222)
            return bad_request(message)
    return inner

