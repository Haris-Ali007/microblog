from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth

@bp.route('/token', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().generate_token()
    db.session.commit()
    return {'token': token}

@bp.route('/token', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    token_auth.current_user().revoke()
    db.session.commit()
    return '', 204
