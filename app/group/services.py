import datetime

from django.core.exceptions import ObjectDoesNotExist

from app.group.models import Group, GroupUser
from app.group.serializers import GroupSerializer

from app.transaction.models import Transaction
from app.transaction.services import TransactionService

from app.user.models import User


class GroupService:
    def get(self, group_id):
        group = Group.objects.get(pk=group_id)
        group.group_users = [User.objects.get(pk=group_user.user.id) for group_user in GroupUser.objects.filter(group_id=group_id)]

        serializer = GroupSerializer(instance=group)

        return serializer.data

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

        for transaction in Transaction.objects.filter(group=Group.objects.get(id=group_id)).order_by('-created_date'):
            transactions = transaction_service.get(transaction.id)
            transactions_dict.append(transactions)

        return transactions_dict


class UserGroupService:
    def get(self, user_id, since_last_login):
        group_service = GroupService()

        date = datetime.datetime.strptime('2017-01-01', '%Y-%m-%d')

        if since_last_login is True:
            user = User.objects.get(pk=user_id)
            date = user.last_login

        groups = Group.objects.filter(
            _group_users__user=user_id,
            created_date__gte=date
        ).order_by('-created_date')

        return [group_service.get(group_id=group.id) for group in groups]
