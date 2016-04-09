from flask import make_response, jsonify

STATUS_CODE_DEFINITIONS = {
    200: "OK",
    201: "Created",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    422: "Unprocessable Entity",
    501: "Not Implemented",
}


def _make_response_with_message(status_code, message=None, errors=None):
    code_def = STATUS_CODE_DEFINITIONS[status_code]
    status = "{}".format(code_def)
    rv = dict(status=status)
    if message:
        rv["message"] = message
    if errors:
        rv["errors"] = errors
    return make_response(jsonify(rv), status_code)


def ok(message=None):
    return _make_response_with_message(200, message=message)


def created(message=None):
    return _make_response_with_message(201, message=message)


def bad_request(message=None, errors=None):
    return _make_response_with_message(400, message=message, errors=errors)


def unauthorized(message=None, errors=None):
    return _make_response_with_message(401, message=message, errors=errors)


def forbidden(message=None, errors=None):
    return _make_response_with_message(403, message=message, errors=errors)


def not_found(message=None, errors=None):
    return _make_response_with_message(404, message=message, errors=errors)


def unprocessable_entity(message=None, errors=None):
    return _make_response_with_message(422, message=message, errors=errors)


def not_implemented(message=None, errors=None):
    return _make_response_with_message(501, message=message, errors=errors)


def with_message(status_code, message=None, errors=None):
    return _make_response_with_message(status_code, message, errors)


def with_target(target):
    return make_response(jsonify(target), 200)


def with_targets(targets):
    """Wrapper JSON array in JSON object."""
    rv = dict(count=0, targets=targets)
    rv["count"] = len(rv["targets"])
    return make_response(jsonify(rv), 200)
