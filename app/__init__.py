from flask import Flask, g
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/pihome'
app.config['SECRET_KEY'] = 'PiHome_pawlus_secret_key'
app.config['DEBUG'] = True

from .api_v1 import api as api_v1_blueprint
app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')
