from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

def create_app():

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/pihome'
    app.config['SECRET_KEY'] = 'PiHome_pawlus_secret_key'
    app.config['DEBUG'] = True

    from .models.user import User

    db.create_all()
    db.session.commit()

    from .api_v1 import api as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    return app
