from . import db

class Device(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    pin = db.Column(db.Integer, nullable=False, unique=True)

    state = db.Column(db.Boolean(), nullable=False, default=False)

    def __init__(self, name, description, pin, state):

        self.name = name
        self.description = description
        self.pin = pin
        self.state = state

    def __init__(self, name, description, pin):

        self.name = name
        self.description = description
        self.pin = pin
