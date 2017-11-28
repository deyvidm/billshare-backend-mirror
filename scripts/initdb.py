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
    r = requests.post(base + "/transaction/", data=json.dumps(data))
    response = json.loads(r.text)
    if 'error' in response:
        return response
    return response.get("id")


user_1 = create_user("tormund", "giantsbane")
user_2 = create_user("sandor", "clegane")
user_3 = create_user("jon", "snow")

group_1 = create_group("frozen cunts", "tormund@test.ca", ["jon@test.ca", "sandor@test.ca"])

#
# user_1 = 1
# user_2 = 2
# user_3 = 3
# group_1 = 1


# trans_id = create_transaction({
#     "total": 100,
#     "currency_code": "CAD",
#     "label": "User 1 owes User 2",
#     "group": group_1,
#     "creator": user_1,
#     "split_type": "money",
#     "user_shares": [
#         {
#             "user": user_1,
#             "owes": 40,
#             "paid": 30
#         },
#         {
#             "user": user_2,
#             "owes": 60,
#             "paid": 70
#         },
#     ]
# })
# print "transaction with id {} successfully created".format(trans_id)
#
# trans_id = create_transaction({
#     "total": 100,
#     "currency_code": "CAD",
#     "label": "User 2 owes User 3",
#     "group": group_1,
#     "creator": user_2,
#     "split_type": "money",
#     "user_shares": [
#         {
#             "user": user_2,
#             "owes": 90,
#             "paid": 30
#         },
#         {
#             "user": user_3,
#             "owes": 10,
#             "paid": 70
#         },
#     ]
# })
# print "transaction with id {} successfully created".format(trans_id)
