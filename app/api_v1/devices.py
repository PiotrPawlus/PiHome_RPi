from flask import jsonify, request, abort, Response
import json

from . import api
from .. import auth
from Error import already_exists, validation, not_authorized

from ..models.device import Device, db

@api.route('/device/<int:id>', methods=['DELETE', 'GET', 'POST'])
@auth.login_required
def get_device(id):

    device = Device.query.filter_by(id = id).first()

    if not device:
        abort(400)

    if request.method == 'DELETE':

        db.session.delete(device)
        db.session.commit()

        return jsonify({
            'status': 200
        }), 200

    if request.method == 'GET':

        return jsonify({

            'name': device.name,
            'description': device.description,
            'id': device.id,
            'pin': device.pin,
            'state': device.state
        }), 201

    if request.method == 'POST':

        name = request.json.get('name')
        description = request.json.get('description')
        pin = request.json.get('pin')

        if name is None or description is None or pin is None:
            return validation

        device.name = name
        device.description = description
        device.pin = pin
        device.state = False

        db.session.commit()

        return jsonify({

            'name': device.name,
            'description': device.description,
            'id': device.id,
            'pin': device.pin,
            'state': device.state
        }), 201

@api.route('/device', methods=['POST'])
@auth.login_required
def create_device():

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
        'id': device.id,
        'pin': device.pin,
        'state': device.state
    }), 201

@api.route('/device/<int:id>/state', methods=['GET', 'POST'])
@auth.login_required
def get_device_state(id):

    device = Device.query.filter_by(id = id).first()

    if request.method == 'GET':

        return jsonify({

            'state': device.state
        }), 200

    if request.method == 'POST':

        device.state = not device.state
        db.session.commit()

        return jsonify({

            'name': device.name,
            'description': device.description,
            'id': device.id,
            'pin': device.pin,
            'state': device.state
        }), 201

@api.route('/devices', methods=['GET'])
@auth.login_required
def get_devices():

    devices = Device.query.all()

    devices_list = []
    for device in devices:

        devices_list.append({

            'name': device.name,
            'description': device.description,
            'id': device.id,
            'pin': device.pin,
            'state': device.state
        })

    devices = {'devices': devices_list}
    return Response(json.dumps(devices), mimetype='application/json')
