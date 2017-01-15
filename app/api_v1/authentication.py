from flask import jsonify, json, request, abort, Response

from . import api
from Error import already_exists, validation, not_authorized
from ..models.user import User
from .. import db, auth, g

@auth.verify_password
def verify_password(username_or_token, password):

    user = User.verify_auth_token(username_or_token)

    if not user:
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False

    g.user = user
    return True

@api.route('/registration', methods=['POST'])
def register():

    if not request.is_json:
        abort(404)

    username = request.json.get('username')
    password = request.json.get('password')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')

    if username is None or password is None or first_name is None or last_name is None:
        return validation(request)

    user = User(username, password, first_name, last_name)

    if db.session.query(db.exists().where(User.username == user.username)).scalar():
        return already_exists('The username already registered.')

    user.hash_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({ 'status': 201 }), 201

@api.route('/authentication', methods=['POST'])
def create_session():

    if not request.is_json:
        abort(404)

    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        return validation(request)

    if not verify_password(username, password):
        return not_authorized

    token = g.user.generate_auth_token()

    return jsonify({

        'authentication_token': token,
        'username': g.user.username,
        'first_name': g.user.first_name,
        'last_name': g.user.last_name,
        'is_enabled': g.user.is_enabled,
        'status': 200
    }), 200

@api.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })
