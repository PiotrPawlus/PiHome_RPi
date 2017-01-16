from flask import jsonify, request, abort

from . import api
from .. import auth

@api.route('/device/<int:id>', methods=['GET'])
@auth.login_required
def get_device(id):
    return "GET device %i" % id

@api.route('/device/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_device(id):
    return "DELETE device %i" % id

@api.route('/device/<int:id>', methods=['PUT'])
@auth.login_required
def update_device(id):
    return "PUT device %i" % id

@api.route('/device', methods=['POST'])
@auth.login_required
def create_device():
    return "POST device"

@api.route('/device/status/<int:id>', methods=['GET'])
@auth.login_required
def get_device_status(id):
    return "GET device status %i" % id

@api.route('/devices', methods=['GET'])
@auth.login_required
def get_devices():
    return "GET devices"
