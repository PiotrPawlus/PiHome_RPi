from flask import jsonify, Response, request
from . import api
from .. import app

@api.errorhandler(400)
def api_validation(error=None):

    return jsonify({
        'status': 400,
        'description': error.description,
        'address': request.url
    }), 400

@app.errorhandler(400)
def validation(error=None):

    return jsonify({
        'status': 400,
        'description': error.description,
        'address': request.url
    }), 400

@api.errorhandler(401)
def api_not_authorized(error=None):

    return jsonify({
        'status': 401,
        'description': error.description,
        'address': request.url
    }), 401

@app.errorhandler(401)
def not_authorized(error=None):

    return jsonify({
        'status': 401,
        'description': error.description,
        'address': request.url
    }), 401

@api.errorhandler(403)
def api_not_active(error=None):

    return jsonify({
        'status': 403,
        'description': 'user_not_active',
        'address': request.url
    }), 403

@app.errorhandler(403)
def not_active(error=None):

    return jsonify({
        'status': 403,
        'description': 'user_not_active',
        'address': request.url
    }), 403

@api.errorhandler(404)
def api_not_found(error=None):

    return jsonify({
        'status': 404,
        'description': error.description,
        'address': request.url
    }), 404

@app.errorhandler(404)
def not_found(error=None):

    return jsonify({
        'status': 404,
        'description': error.description,
        'address': request.url
    }), 404

@api.errorhandler(409)
def api_already_exists(error=None):

    return jsonify({

        'status': 409,
        'description': error.description,
        'address': request.url
    }), 409

@app.errorhandler(409)
def already_exists(error=None):

    return jsonify({

        'status': 409,
        'description': error.description,
        'address': request.url
    }), 409

@api.errorhandler(501)
def api_not_implemented(error=None):

    return jsonify({

        'status': 501,
        'description': 'not_implemented',
        'address': request.url
    }), 501

@app.errorhandler(501)
def not_implemented(error=None):

    return jsonify({

        'status': 501,
        'description': 'not_implemented',
        'address': request.url
    }), 501
