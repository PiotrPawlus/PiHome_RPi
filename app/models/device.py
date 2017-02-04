from . import db

class Device(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    pin = db.Column(db.Integer, nullable=False, unique=True)

    device_type = db.Column(db.String(20), nullable=False, default='switch')

    def __init__(self, name, description, pin, device_type):

        self.name = name
        self.description = description
        self.pin = pin
        self.device_type = device_type
        
