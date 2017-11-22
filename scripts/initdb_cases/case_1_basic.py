from helpers import *


class Case1:
    user_1 = 1
    user_2 = 2
    user_3 = 3
    group_1 = 1

    def execute(self, create_users=True, create_groups=True):
        if create_users:
            self.create_users()
        if create_groups:
            self.create_groups()

        self.create_transactions()

    def create_users(self):
        self.user_1 = create_user("tormund", "giantsbane")
        self.user_2 = create_user("sandor", "clegane")
        self.user_3 = create_user("jon", "snow")

    def create_groups(self):
        self.group_1 = create_group("frozen cunts", "tormund@test.ca", ["jon@test.ca", "sandor@test.ca"])

    def create_transactions(self):
        trans_id = create_transaction({
            "total": 100,
            "currency_code": "CAD",
            "label": "User 1 owes User 2",
            "group": self.group_1,
            "creator": self.user_1,
            "split_type": "money",
            "user_shares": [
                {
                    "user": self.user_1,
                    "owes": 40,
                    "paid": 30
                },
                {
                    "user": self.user_2,
                    "owes": 60,
                    "paid": 70
                },
            ]
        })
        print "transaction with id {} successfully created".format(trans_id)

        trans_id = create_transaction({
            "total": 100,
            "currency_code": "CAD",
            "label": "User 2 owes User 3",
            "group": self.group_1,
            "creator": self.user_2,
            "split_type": "money",
            "user_shares": [
                {
                    "user": self.user_2,
                    "owes": 90,
                    "paid": 30
                },
                {
                    "user": self.user_3,
                    "owes": 10,
                    "paid": 70
                },
            ]
        })
        print "transaction with id {} successfully created".format(trans_id)
