from flask_sqlalchemy import SQLAlchemy
from .. import app

db = SQLAlchemy(app)

from .user import User

db.create_all()
db.session.commit()
