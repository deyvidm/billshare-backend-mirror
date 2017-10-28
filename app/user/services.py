from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

from app.transaction_line_item.services import TransactionLineItemService
from app.transaction_line_item.models import TransactionLineItem
from app.user.models import User


class UserService:

    def get(self, user_id):
        return User.objects.get_user({'pk': user_id})

    def create(self, email, password, first_name, last_name):
        return User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)

    def update(self, user_id, updated_fields):
        return User.objects.update_user({'pk': user_id}, updated_fields)

    def delete(self, user_id):
        return User.objects.delete_user({'pk': user_id})

    def email_exists(self, email):

        try:
            User.objects.get_user({'email': email})
        except ObjectDoesNotExist:
            return False

        return True


class UserTransactionService:
    def get(self, user_id):
        transaction_line_item_service = TransactionLineItemService()
        transactions = TransactionLineItem.objects.filter(
            Q(payer=User.objects.get(id=user_id)) |
            Q(payee=User.objects.get(id=user_id))
        )

        transaction_ids = sorted(set([t.transaction.id for t in transactions]))

        transactions_dict = []
        for transaction_id in transaction_ids:
            transaction = transaction_line_item_service.get(transaction_id)
            transactions_dict.append(transaction)

        return transactions_dict
