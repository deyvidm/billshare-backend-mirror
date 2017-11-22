import requests
import json
import collections

base = "http://127.0.0.1:3000"


def post_to_api(url, data):
    r = requests.post(url, json.dumps(data))
    response = json.loads(r.text)
    if 'error' in response:
        print "\n==[ data ]=="
        print data
        raise Exception(response.get('error'))
    return response


def create_group(label, creator, members):
    data = {
        "label": label,
        "creator": creator,
        "group_users": members
    }
    return post_to_api(base + "/group/", data).get("id")


def create_user(first, last="Test"):
    data = {
        "email": first + "@test.ca",
        "password": first,
        "first_name": first,
        "last_name": last
    }
    return post_to_api(base + "/auth/create/", data).get('id')


def create_transaction(data):
    return post_to_api(base + "/transaction/", data).get('id')
