import requests
import json

base = "http://127.0.0.1:3000"


def create_group(label, creator, members):
    data = {
        "label": label,
        "creator": creator,
        "group_users": members
    }
    r = requests.post(base + "/group/", data=json.dumps(data))
    return json.loads(r.text)['id']


def create_user(first, last="Test"):
    data = {
        "email": first + "@test.ca",
        "password": first,
        "first_name": first,
        "last_name": last
    }
    r = requests.post(base + "/auth/create/", data=json.dumps(data))
    response = json.loads(r.text)
    if 'error' in response and response['error'] == "Email already exists":
        exit(0)
    return response.get("id")


def create_transaction(data):
    r = requests.post(base + "/transaction/", data=data)
    return json.loads(r.text)


# user_1 = create_user("tormund", "giantsbane")
# user_2 = create_user("sandor", "clegane")
# user_3 = create_user("jon", "snow")
#
# group_1 = create_group("frozen cunts", "tormund@test.ca", ["jon@test.ca", "sandor@test.ca"])

user_1 = 1
user_2 = 2
user_3 = 3
group_1 = 1


create_transaction({
    "total": 300,
    "currency_code": "CAD",
    "label": "testLabel",
    "group": group_1,
    "creator": user_1,
    "split_type": "percent",
    "user_shares": [
        {
            "user": user_1,
            "owes": 33.33,
            "paid": 100
        },
        {
            "user": user_2,
            "owes": 33.33,
            "paid": 100
        },
        {
            "user": user_3,
            "owes": 33.34,
            "paid": 100
        }
    ]
})
