from flask import jsonify, json, request, abort, Response
import RPi.GPIO as GPIO
import time

from . import api
from ..models.device import Device, db
from .. import auth, g

all_devices = Device.query.all()

GPIO.setmode(GPIO.BCM)

for device in all_devices:
    GPIO.setup(int(device.pin), GPIO.OUT)

    if device.device_type == 'button':
        GPIO.output(int(device.pin), GPIO.HIGH)
    elif device.device_type == 'switch':
        GPIO.output(int(device.pin), GPIO.LOW)

@api.route('/device/<int:id>', methods=['DELETE', 'GET'])
@auth.login_required
def get_delete_device(id):

    device = Device.query.filter_by(id = id).first()

    if not device:
        return abort(400, 'Device not found.')

    state = -1

    try:
        state = device_state(device.pin)
    except:
        return abort(400, 'Device is not connected.')

    if request.method == 'GET':

        return jsonify({

            'name': device.name,
            'description': device.description,
            'id': device.id,
            'pin': device.pin,
            'state': state,
            'type': device.device_type
        }), 200

    if not g.user.administrator:
        return abort(400, 'Device not found.')

    if request.method == 'DELETE':

        state = -1

        try:
            state = device_state(device.pin)
        except:
            return abort(400, 'Device is not connected.')

        if state == 0 and device.device_type == 'button':
            GPIO.output(int(device.pin), GPIO.HIGH)

        if state == 1 and device.device_type == 'switch':
            GPIO.output(int(device.pin), GPIO.LOW)

        GPIO.cleanup(int(device.pin))

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
        device_type = request.json.get('type')
        pin = request.json.get('pin')

        if name is None or description is None or pin is None or device_type is None:
            return abort(404, 'Missing argumets in request for ' + request.url)

        if not name or not pin:
            return abort(400, 'Name and pin cannot be empty.')

        device = Device.query.filter_by(pin = pin).first()

        if device:
            return abort(409, 'The device already added to system.')

        device = Device(name, description, pin, device_type)

        GPIO.setup(int(device.pin), GPIO.OUT)

        if device.device_type == 'button':
            GPIO.output(int(device.pin), GPIO.HIGH)

        elif device.device_type == 'switch':
            GPIO.output(int(device.pin), GPIO.LOW)

        state = -1

        try:
            state = device_state(device.pin)
        except:
            return abort(400, 'Device is not connected.')

        db.session.add(device)
        db.session.commit()

        return jsonify({

            'name': device.name,
            'description': device.description,
            'id': device.id,
            'pin': device.pin,
            'state': state,
            'type': device.device_type
        }), 201

    return abort(404, 'Not found: ' + request.url)

@api.route('/device/<int:id>/state', methods=['GET', 'POST'])
@auth.login_required
def get_set_device_state(id):

    device = Device.query.filter_by(id = id).first()

    if not device:
        abort(400, 'Device not found.')

    if request.method == 'GET':

        state = -1

        try:
            state = device_state(device.pin)
        except:
            return abort(400, 'Device is not connected.')

        return jsonify({

            'name': device.name,
            'description': device.description,
            'id': device.id,
            'pin': device.pin,
            'state': state,
            'type': device.device_type
        }), 200

    if request.method == 'POST':

        if device.device_type == 'switch':

            state = -1

            try:
                state = device_state(device.pin)
            except:
                return abort(400, 'Device is not connected.')

            if state == 1:
                GPIO.output(int(device.pin), GPIO.LOW)
            elif state == 0:
                GPIO.output(int(device.pin), GPIO.HIGH)

            try:
                state = device_state(device.pin)
            except:
                return abort(400, 'Device is not connected.')

            return jsonify({

                'name': device.name,
                'description': device.description,
                'id': device.id,
                'pin': device.pin,
                'state': state,
                'type': device.device_type
            }), 201

        elif device.device_type == 'button':

            GPIO.output(int(device.pin), GPIO.LOW)
            time.sleep(2)
            GPIO.output(int(device.pin), GPIO.HIGH)

            return jsonify({

                'name': device.name,
                'description': device.description,
                'id': device.id,
                'pin': device.pin,
                'state': False,
                'type': device.device_type
            }), 201

        return abort(501)

@api.route('/devices', methods=['GET'])
@auth.login_required
def get_devices():

    devices = Device.query.all()

    devices_list = []
    for device in devices:

        state = -1

        try:
            state = device_state(device.pin)
        except:
            return abort(400, 'Device is not connected.')

        devices_list.append({

            'name': device.name,
            'description': device.description,
            'id': device.id,
            'pin': device.pin,
            'state': state,
            'type': device.device_type
        })

    devices = {'devices': devices_list}
    return Response(json.dumps(devices), mimetype='application/json')

def device_state(pin):
    return GPIO.input(int(pin))
