from flask import jsonify, json, request, abort, Response

from . import api
from Error import already_exists
from ..models.user import User
from .. import db

@api.route('/registration', methods=['POST'])
def register():

    user = User(request.form['email'], request.form['password'], request.form['first_name'], request.form['last_name'])

    exists = db.session.query(db.exists().where(User.email == user.email)).scalar()

    if exists:
        return already_exists('The email already registered.')

    db.session.add(user)
    db.session.commit()

    return Response('', status=201, mimetype='application/json')

@api.route('/session', methods=['POST'])
def create_session():
    return "Session Created"

@api.route('/session', methods=['DELETE'])
def delete_session():
    return "Session Deleted"
