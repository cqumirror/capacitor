import requests
import json
import os

curr_path = os.path.abspath(os.curdir)
os.environ["CAPACITOR_SETTINGS"] = \
    os.path.join(curr_path, "settings_local.cfg")

from capacitor import settings_get
from capacitor import security


def json_post_for_dev(token):
    base_url = "http://localhost:5000/api"
    mirrors_url = "{}/mirrors".format(base_url)
    notices_url = "{}/notices".format(base_url)

    headers = {"Authorization": "Token {}".format(token)}
    with open("data_local/mirrors.json", "r") as json_data_file:
        json_data = dict(
            targets=json.load(json_data_file),)
        resp = requests.post(mirrors_url, json=json_data, headers=headers)
        print resp.status_code

    with open("data_local/notices.json", "r") as json_data_file:
        json_data = dict(
            targets=json.load(json_data_file),)
        resp = requests.post(notices_url, json=json_data, headers=headers)
        print resp.status_code


def init_users():
    import redis
    params = dict(
        host=settings_get("REDIS_HOST"),
        port=settings_get("REDIS_PORT"),
        db=settings_get("REDIS_DB"))
    r = redis.StrictRedis(**params)
    users = {
        "porter": {}
    }
    r.set("users", json.dumps(users))


def grant_access_token():
    secret_key = settings_get("SECRET_KEY")
    _token = security.create_signed_value(
        secret_key, "client_id", "porter")
    value = security.decode_signed_value(
        secret_key, "client_id", _token,
        settings_get("signature_expiration"))
    return _token


if __name__ == '__main__':
    init_users()
    token = grant_access_token()
    json_post_for_dev(token)
