from flask import jsonify, json, request, abort, Response

from . import api
from ..models.device import Device, db
from .. import auth, g

@api.route('/device/<int:id>', methods=['DELETE', 'GET'])
@auth.login_required
def get_update_delete_device(id):

    device = Device.query.filter_by(id = id).first()

    if not device:
        return abort(400, 'Device not found.')

    if request.method == 'GET':

        return jsonify({

            'name': device.name,
            'description': device.description,
            'id': device.id,
            'pin': device.pin,
            'state': device.state
        }), 200

    if not g.user.administrator:
        return abort(400, 'Device not found.')

    if request.method == 'DELETE':

        db.session.delete(device)
        db.session.commit()

        return jsonify({
            'status': 200
        }), 200

@api.route('/device', methods=['POST'])
@auth.login_required
def create_device():

    if g.user.administrator:

        name = request.json.get('name')
        description = request.json.get('description')
        pin = request.json.get('pin')

        if name is None or description is None or pin is None:
            return abort(404, 'Missing argumets in request for ' + request.url)

        if not name or not pin:
            return abort(400, 'Name and pin cannot be empty.')

        device = Device(name, description, pin)

        # if db.session.query(db.exists().where(Device.pin == device.pin)).scalar():
        #     return abort(409, 'The device already added to system.')

        db.session.add(device)
        db.session.commit()

        return jsonify({

            'name': device.name,
            'description': device.description,
            'id': device.id,
            'pin': device.pin,
            'state': device.state
        }), 201

    return abort(404, 'Not found: ' + request.url)

@api.route('/device/<int:id>/state', methods=['GET', 'POST'])
@auth.login_required
def get_set_device_state(id):

    device = Device.query.filter_by(id = id).first()

    if not device:
        abort(400, 'Device not found.')

    if request.method == 'GET':

        return jsonify({

            'name': device.name,
            'description': device.description,
            'id': device.id,
            'pin': device.pin,
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
