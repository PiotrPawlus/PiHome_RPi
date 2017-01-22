from flask import jsonify, json, request, abort, Response

from . import api
from Error import already_exists, validation, not_authorized
from ..models.user import User, db
from .. import auth, g

@auth.verify_password
def verify_password(email_or_token, password):

    user = User.verify_auth_token(email_or_token)
    if not user:

        user = User.query.filter_by(email = email_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@api.route('/baseurl', methods=['GET'])
def connect():

    return jsonify({
        'url': request.url
    }), 200

@api.route('/registration', methods=['POST'])
def register():

    if not request.is_json:
        abort(404)

    email = request.json.get('email')
    password = request.json.get('password')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')

    if email is None or password is None or first_name is None or last_name is None:
        return validation(request)

    user = User(email, password, first_name, last_name)

    if db.session.query(db.exists().where(User.email == user.email)).scalar():
        return already_exists('The email already registered.')

    user.hash_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({

        'authentication_token': '',
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_authorized': user.is_authorized,
        'status': 201
    }), 201

@api.route('/authentication', methods=['POST'])
def create_session():

    if not request.is_json:
        abort(404)

    email = request.json.get('email')
    password = request.json.get('password')

    if email is None or password is None:
        return validation()

    if not verify_password(email, password):
        return not_authorized

    if not g.user.is_authorized:
        return not_active()

    token = g.user.generate_auth_token()

    return jsonify({

        'authentication_token': token,
        'email': g.user.email,
        'first_name': g.user.first_name,
        'last_name': g.user.last_name,
        'is_authorized': g.user.is_authorized,
        'status': 200
    }), 200

@api.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })
