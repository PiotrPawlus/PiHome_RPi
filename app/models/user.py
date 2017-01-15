from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from .. import app, db, auth

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    access_token = db.Column(db.String(16), nullable=True)
    is_enabled = db.Column(db.Boolean(), nullable=False, default=False)

    def __init__(self, username, password, first_name, last_name, is_enabled):

        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.is_enabled = is_enabled

    def __init__(self, username, password, first_name, last_name):

        self.username = username
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<User %r>' % self.username

    def is_active(self):
      return self.is_enabled

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user
