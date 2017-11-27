import datetime
from django.core.exceptions import ObjectDoesNotExist

from app.group.services import UserGroupService
from app.transaction.services import UserTransactionService, TransactionService
from app.user.models import User
from app.user.serializers import UserSerializer


class UserService:
    def get(self, user_id):
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(instance=user)

        return serializer.data

    def create(self, email, password, first_name, last_name):
        return User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)

    def update(self, user_id, updated_fields):
        return User.objects.update_user({'pk': user_id}, updated_fields)

    def delete(self, user_id):
        return User.objects.delete_user({'pk': user_id})

    def email_exists(self, email):

        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return False

        return True


class DashboardService:

    user_group_service = UserGroupService()
    user_transaction_service = UserTransactionService()
    transaction_service = TransactionService()

    def get(self, user_id):
        groups = self.user_group_service.get(user_id, True)
        user = User.objects.get(pk=user_id)
        transactions = self.user_transaction_service.get_transactions_in_range(
            user_id,
            user.last_login,
            datetime.datetime.utcnow()
        )

        transactions = [self.transaction_service.get(t.id) for t in transactions]

        return {
            "groups": groups,
            "transactions": transactions
        }
