from flask import jsonify, g, make_response
from app import db
from app.api import bp
from app.api.auth import basic_auth,token_auth
from app.model.models import User



@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_jwt()
    db.session.commit()
    resp = make_response()
    resp.set_cookie('jwt',token)
    return resp


