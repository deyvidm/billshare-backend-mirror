from django.forms import model_to_dict
from django.core.exceptions import ObjectDoesNotExist

from app.group.models import Group, GroupUser

from app.transaction.models import Transaction
from app.transaction.services import TransactionService

from app.user.models import User
from app.user.services import UserService


class GroupService:
    def get(self, group_id):
        user_service = UserService()

        group = Group.objects.get(pk=group_id)
        group_users = GroupUser.objects.filter(group=group)

        users = []
        for user in group_users:
            users.append(user_service.get(user.user_id))

        creator = user_service.get(group.creator.id)

        excluded_fields = [
            'creator',
        ]

        group_dict = model_to_dict(instance=group, exclude=excluded_fields)
        group_dict['group_users'] = users

        return group_dict

    def create(self, label, creator_email, user_emails):
        try:
            creator = User.objects.get(email=creator_email)
        except ObjectDoesNotExist:
            return None

        if creator_email not in user_emails:
            user_emails.append(creator_email)

        valid_users = []
        for email in user_emails:
            try:
                user = User.objects.get(email=email)
                valid_users.append(user)
            except ObjectDoesNotExist:
                pass

        if len(valid_users) == 1:
            return None

        group = Group.objects.create(label=label, creator=creator)

        for user in valid_users:
            GroupUser.objects.create(group=group, user=user)

        return self.get(group.id)

    def update(self, group_id, updated_fields):
        Group.objects.filter(pk=group_id).update(updated_fields)

    def delete(self, group_id):
        Group.objects.get(pk=group_id).delete()

    def get_transactions(self, group_id):
        transaction_service = TransactionService()

        transactions_dict = []

        for transaction in Transaction.objects.filter(group=Group.objects.get(id=group_id)):
            transactions = transaction_service.get(transaction.id)
            transactions_dict.append(transactions)

        return transactions_dict


class GroupUserService:
    def get(self, user_id):
        group_service = GroupService()
        user = User.objects.get(id=user_id)
        group_objects = GroupUser.objects.filter(user=user).values('group')
        groups_formatted = []

        for group in group_objects:
            groups_formatted.append(group_service.get(group['group']))

        return groups_formatted
