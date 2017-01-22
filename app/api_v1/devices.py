from flask import jsonify, request, abort

from . import api
from .. import auth
from Error import already_exists, validation, not_authorized

from ..models.device import Device, db



@api.route('/device/<int:id>', methods=['DELETE', 'GET', 'UPDATE'])
def get_device(id):

    if not request.is_json:
        abort(404)

    if request.method == 'DELETE':
        print('DELETE')
    if request.method == 'GET':
        print('GET')
    if request.method == 'UPDATE':
        print('UPDATE')

@api.route('/device', methods=['POST'])
def create_device():

    if not request.is_json:
        abort(404)

    name = request.json.get('name')
    description = request.json.get('description')
    pin = request.json.get('pin')

    if name is None or description is None or pin is None:
        return validation

    device = Device(name, description, pin)

    if db.session.query(db.exists().where(Device.pin == device.pin)).scalar():
        return already_exists('The device already registered.')

    db.session.add(device)
    db.session.commit()

    return jsonify({

        'name': device.name,
        'description': device.description,
        'pin': device.pin,
        'state': device.state,
        'status': 201
    }), 201

@api.route('/device/status/<int:id>', methods=['GET'])
def get_device_status(id):
    return "GET device status %i" % id

@api.route('/devices', methods=['GET'])
def get_devices():
    return "GET devices"
