import requests
import json


def json_post_for_dev():
    base_url = "http://localhost:5000/api"
    mirrors_url = "{}/mirrors".format(base_url)
    notices_url = "{}/notices".format(base_url)

    headers = [("Content-Type", "application/json")]
    with open("data/mirrors.json", "r") as json_data_file:
        json_data = json.load(json_data_file)
        resp = requests.post(mirrors_url, json=json_data)
        print resp.status_code

    with open("data/notices.json", "r") as json_data_file:
        json_data = json.load(json_data_file)
        resp = requests.post(notices_url, json=json_data)
        print resp.status_code


if __name__ == '__main__':
    json_post_for_dev()
