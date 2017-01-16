from flask import jsonify, Response
from . import api

def validation():

    return jsonify({
        'status': 400,
        'description': 'Invalid request\'s values',
    }), 400


def already_exists(description=''):

    return jsonify({

        'status': 409,
        'description': description
    }), 409

def not_authorized():

    return jsonify({

        'status': 401,
        'description': 'Not authorized.'
    }), 401

def not_active():

    return jsonify({

        'status': 401,
        'description': 'Wait for acceptance.'
    })
