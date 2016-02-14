from flask import make_response, jsonify


def not_found(error_message="not found"):
    rv = dict(message=error_message, code=404)
    resp = make_response(jsonify(rv), 404)
    return resp
