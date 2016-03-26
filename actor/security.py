from flask import request
from actor import response


def authenticated(func):
    """Authentication."""
    def wrapper(*args, **kwargs):
        # args[0] is self
        self = args[0]
        if not self.current_user:
            return response.unauthorized()
        return func(*args, **kwargs)
    return wrapper


def create_signed_value(secret_key, name, value):
    pass


def decode_signed_value(secret_key, name, value):
    pass
