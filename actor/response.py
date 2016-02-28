from flask import make_response, jsonify

STATUS_CODE_DEFINITIONS = {
    201: "Created",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    422: "Unprocessable Entity",
    501: "Not Implemented",
}


def make_resp(status_code, message=None, errors=None):
    code_def = STATUS_CODE_DEFINITIONS[status_code]
    status = "{} {}".format(status_code, code_def)
    rv = dict(status=status)
    if message:
        rv["message"] = message
    if errors:
        rv["errors"] = errors
    resp = make_response(jsonify(rv), status_code)
    return resp


def created(message=None):
    return make_resp(201, message=message)


def bad_request(message=None, errors=None):
    return make_resp(400, message=message, errors=errors)


def unauthorized(message=None, errors=None):
    return make_resp(401, message=message, errors=errors)


def forbidden(message=None, errors=None):
    return make_resp(403, message=message, errors=errors)


def not_found(message=None, errors=None):
    return make_resp(404, message=message, errors=errors)


def unprocessable_entity(message=None, errors=None):
    return make_resp(422, message=message, errors=errors)


def not_implemented(message=None, errors=None):
    return make_resp(501, message=message, errors=errors)

