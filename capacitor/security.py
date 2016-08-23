import time
import base64
import hmac
import hashlib
from functools import wraps
from flask import request
import redis

from capacitor import app
from capacitor import settings_get
from capacitor import response


def get_secret_key():
    secret = settings_get("secret_key")
    return secret


def parse_header_auth(value):
    # unicode to str
    v = str(value)
    # e.g. Authorization: Token access_token
    token = v.split()[1].strip()
    return token


def get_access_token():
    if "Authorization" not in request.headers:
        return None
    access_token = parse_header_auth(request.headers["Authorization"])
    return access_token


def get_redis():
    conn = redis.StrictRedis(host=settings_get("REDIS_HOST"),
                             port=settings_get("REDIS_PORT"),
                             db=settings_get("REDIS_DB"))
    return conn


def test_current_user():
    _access_token = get_access_token()
    _secret_key = get_secret_key()
    if not _access_token or not _secret_key:
        return None
    expiration = settings_get("access_token_expiration")
    args = (_secret_key, "access_token", _access_token, expiration)
    current_user = decode_signed_value(*args)
    _redis = get_redis()
    users_cached = _redis.get("users")
    if not users_cached or current_user not in users_cached.keys():
        return None
    return current_user


def authenticated(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not test_current_user():
            return response.forbidden()
        return func(*args, **kwargs)
    return decorated


def _create_signature(secret, *parts):
    _hash = hmac.new(secret, digestmod=hashlib.sha256)
    for part in parts:
        _hash.update(part)
    return _hash.hexdigest()


def create_signed_value(secret, name, value):
    wall_clock = time.time
    timestamp = str(int(wall_clock()))
    value = base64.b64encode(value)

    signature = _create_signature(secret, name, value, timestamp)
    return '|'.join([value, timestamp, signature])


def _time_independent_equals(a, b):
    return hmac.compare_digest(a, b)


def decode_signed_value(secret, name, value, max_age_days):
    wall_clock = time.time
    parts = value.split('|')
    if len(parts) != 3:
        return None
    signature = _create_signature(secret, name, parts[0], parts[1])
    if not _time_independent_equals(parts[2], signature):
        app.logger.warning("invalid cookie signature {}".format(value))
        return None
    timestamp = int(parts[1])
    if timestamp < wall_clock() - max_age_days * 86400:
        app.logger.warning("expired cookie {}".format(value))
    try:
        return base64.b64decode(parts[0])
    except Exception:
        return None

