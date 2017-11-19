import requests
import json

base = "http://127.0.0.1:3000"


def create_group(label, creator, members):
    data = {
        "label": label,
        "creator": creator,
        "group_users": members
    }
    requests.post(base + "/group/", data=json.dumps(data))


def create_user(first, last="Test"):
    data = {
        "email": first + "@test.ca",
        "password": first,
        "first_name": first,
        "last_name": last
    }
    requests.post(base + "/auth/create/", data=json.dumps(data))


create_user("tormund", "giantsbane")
create_user("sandor", "clegane")
create_user("jon", "snow")

create_group("frozen cunts", "tormund@test.ca", ["jon@test.ca", "sandor@test.ca"])
