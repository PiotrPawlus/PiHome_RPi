from flask import jsonify, json, request, abort, Response

from . import api
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

@api.route('/', methods=['GET'])
def connect():

    return jsonify({
        'url': request.url
    }), 200

@api.route('/registration', methods=['POST'])
def register():

    email = request.json.get('email')
    password = request.json.get('password')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')

    if email is None or password is None or first_name is None or last_name is None:
        return abort(404, 'missing_argumets')

    if not email or not password or not first_name or not last_name:
        return abort(400, 'empty_parameters')

    user = User(email, password, first_name, last_name)

    if db.session.query(db.exists().where(User.email == user.email)).scalar():
        return abort(409, 'email_already_registered.')

    user.hash_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({

        'authentication_token': '',
        'email': user.email,
        'first_name': user.first_name,
        'id': user.id,
        'is_authorized': user.is_authorized,
        'last_name': user.last_name,
        'status': 201
    }), 201

@api.route('/authentication', methods=['POST'])
def authentication():

    email = request.json.get('email')
    password = request.json.get('password')

    if email is None or password is None:
        return abort(404, 'missing_argumets')

    if not verify_password(email, password):
        return abort(401, 'wrong_email_or_password')

    if not g.user.is_authorized:
        return abort(403)

    token = g.user.generate_auth_token()

    message = {

        'authentication_token': token,
        'email': g.user.email,
        'first_name': g.user.first_name,
        'id': g.user.id,
        'is_authorized': g.user.is_authorized,
        'last_name': g.user.last_name,
        'status': 200
    }

    if g.user.administrator:
        message['super_user'] = g.user.administrator

    return jsonify(message), 200

@api.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })

@api.route('/users', methods=['GET'])
@auth.login_required
def get_users():

    if not g.user.administrator:
        return abort(404, 'not_found')

    users = User.query.all()

    users_list = []
    for user in users:

        users_list.append({

            'email': user.email,
            'first_name': user.first_name,
            'id': user.id,
            'is_authorized': user.is_authorized,
            'last_name': user.last_name,
            'super_user': user.administrator
        })

    users = {'users': users_list}
    return Response(json.dumps(users), mimetype='application/json')

@api.route('/users/<int:id>/authorization', methods=['POST'])
@auth.login_required
def authorized_user(id):

    if not g.user.administrator:
        return abort(404, 'not_found')

    user = User.query.filter_by(id = id).first()

    if not user:
        abort(400, 'user_not_found')

    if g.user.id == user.id:
        abort(409, 'cannot_update_yourself')

    user.is_authorized = not user.is_authorized
    db.session.commit()

    return jsonify({

        'email': user.email,
        'first_name': user.first_name,
        'id': user.id,
        'is_authorized': user.is_authorized,
        'last_name': user.last_name,
        'super_user': user.administrator
    }), 201

@api.route('/users/<int:id>/administration', methods=['POST'])
@auth.login_required
def set_administration_privilege(id):

    if not g.user.administrator:
        return abort(404, 'not_found')

    user = User.query.filter_by(id = id).first()

    if not user:
        abort(400, 'user_not_found')

    if g.user.id == user.id:
        abort(409, 'cannot_update_yourself')

    user.is_authorized = True
    user.administrator = not user.administrator
    db.session.commit()

    return jsonify({

        'email': user.email,
        'first_name': user.first_name,
        'id': user.id,
        'is_authorized': user.is_authorized,
        'last_name': user.last_name,
        'super_user': user.administrator
    }), 201
