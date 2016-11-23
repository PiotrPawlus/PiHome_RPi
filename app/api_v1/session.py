from flask import jsonify, request, abort

from . import api

@api.route('/session', methods=['POST'])
def create_session():
    return "Session Created"

@api.route('/session', methods=['DELETE'])
def delete_session():
    return "Session Deleted"
