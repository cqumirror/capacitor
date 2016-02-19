from flask import make_response, jsonify


def bad_request(error_message="Bad Request"):
    rv = dict(message=error_message)
    resp = make_response(jsonify(rv), 400)
    return resp


def unauthorized(error_message="Unauthorized"):
    rv = dict(message=error_message)
    resp = make_response(jsonify(rv), 401)
    return resp


def forbidden(error_message="Forbidden"):
    rv = dict(message=error_message)
    resp = make_response(jsonify(rv), 403)
    return resp


def not_found(error_message="Not Found"):
    rv = dict(message=error_message)
    resp = make_response(jsonify(rv), 404)
    return resp


def unprocessable_entity(error_message="Unprocessable Entity",
                         errors=None):
    rv = dict(message=error_message)
    if errors is not None:
        rv["errors"] = errors
    resp = make_response(jsonify(rv), 422)
    return resp


def not_implemented(error_message="Not Implemented"):
    rv = dict(message=error_message)
    resp = make_response(jsonify(rv), 501)
    return resp

