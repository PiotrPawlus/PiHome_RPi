from flask import Flask

def create_app():
    app = Flask(__name__)

    from .api_v1 import api as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    return app
