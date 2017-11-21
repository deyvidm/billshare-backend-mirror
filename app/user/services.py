import datetime


from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.utils import timezone

from app.transaction.services import TransactionService
from app.transaction.models import TransactionLineItem, Transaction
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


class UserTransactionService:
    def get(self, user_id, time_start=None, time_end=None):

        transaction_line_item_service = TransactionService()
        transactions = TransactionLineItem.objects.filter(
            Q(debtor=User.objects.get(id=user_id)) |
            Q(creditor=User.objects.get(id=user_id))
        )
        transaction_ids = sorted(set([t.transaction.id for t in transactions]))

        transactions_dict = []
        for transaction_id in transaction_ids:
            transaction = transaction_line_item_service.get(transaction_id)
            transactions_dict.append(transaction)

        transactions_dict = sorted(transactions_dict, key=lambda t: t['updated_date'], reverse=True)
        return transactions_dict

    def get_summary(self, user_id, time_start=None, time_end=None):
        if not time_end:
            time_end = timezone.now()
        if not time_start:
            time_start = (time_end.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)

        transactions = Transaction.objects.filter(
            Q(created_date__range=[time_start, time_end]) &
            (
                Q(transaction_line_items__debtor=user_id) |
                Q(transaction_line_items__creditor=user_id)
            )
        ).distinct()

        debtTotal = 0
        creditTotal = 0
        user = User.objects.get(pk=user_id)
        transaction_ids = sorted(set([t.id for t in transactions.all()]))
        for transaction_id in transaction_ids:
            transaction = Transaction.objects.get(pk=transaction_id)
            for line_item in transaction.transaction_line_items.all():
                if line_item.debtor == user:
                    debtTotal += line_item.debt
                elif line_item.creditor == user:
                    creditTotal += line_item.debt

        return {
            "total transactions": len(transactions),
            "credit": creditTotal.amount,
            "debt": debtTotal.amount,
            "time_start": time_start,
            "time_end": time_end
        }
