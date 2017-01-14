from .. import db

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    is_enabled = db.Column(db.Boolean(), nullable=False, default=False)

    def __init__(self, email, password, first_name, last_name, is_enabled):

        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.is_enabled = is_enabled

    def __init__(self, email, password, first_name, last_name):

        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.is_enabled = False

    def __repr__(self):
        return '<User %r>' % self.email

    def is_active(self):
      return self.is_enabled
