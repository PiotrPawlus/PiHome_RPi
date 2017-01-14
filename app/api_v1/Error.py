from flask import json, Response
from . import api

def already_exists(description=''):

    error = {
        'status': 409,
        'description': description
    }
    js = json.dumps(error)

    return Response(js, status=409, mimetype='application/json')
