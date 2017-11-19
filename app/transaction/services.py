from django.utils import timezone
from django.db.models import Q

from functools import reduce

from django.forms import model_to_dict
from djmoney.money import Money

from app.group.models import Group

from app.transaction.models import Transaction
from app.transaction.models import TransactionLineItem
from app.transaction.serializers import TransactionSerializer

from app.user.models import User


class TransactionService:
    def create_transaction(self, creator_id, group_id, user_shares, total, currency_code, label):

        paid_total = reduce(lambda x, y: x + y, [t['paid'] for t in user_shares])
        owes_total = reduce(lambda x, y: x + y, [t['owes'] for t in user_shares])

        if paid_total != owes_total or owes_total != total:
            # TODO Custom Exception
            return None

        transaction = Transaction.objects.create(
            label=label,
            group_id=group_id,
            creator_id=creator_id,
        )

        paid_shares = [{'user': t['user'], 'share': t['paid']} for t in user_shares if t['paid']]
        owes_shares = [{'user': t['user'], 'share': t['owes']} for t in user_shares if t['owes']]

        while paid_shares and owes_shares:

            paid_shares.sort(key=lambda t: t['user'], reverse=True)
            owes_shares.sort(key=lambda t: t['user'], reverse=True)

            paid_pair, owes_pair = next(((a, b) for a in paid_shares for b in owes_shares if a['user'] == b['user']), ({}, {}))

            if paid_pair and owes_pair:
                paid_shares = [a for a in paid_shares if a['user'] != paid_pair['user']]
                owes_shares = [a for a in owes_shares if a['user'] != owes_pair['user']]
            else:
                paid_pair = paid_shares.pop()
                owes_pair = owes_shares.pop()

            if owes_pair['share'] > paid_pair['share']:
                debt = paid_pair['share']
                owes_pair['share'] -= debt
                owes_shares.append(owes_pair)
            else:
                debt = owes_pair['share']
                paid_pair['share'] -= debt
                if paid_pair['share']:
                    paid_shares.append(paid_pair)

            resolved = owes_pair['user'] == paid_pair['user']

            TransactionLineItem.objects.create(
                transaction=transaction,
                group_id=group_id,
                debtor_id=owes_pair['user'],
                creditor_id=paid_pair['user'],
                debt=Money(debt, currency_code),
                resolved=resolved,
            )

        Group.objects.filter(
            pk=transaction.group_id,
        ).update(updated_date=timezone.now())

        return self.get(transaction_id=transaction.id)

    def get(self, transaction_id):
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.transaction_line_items = TransactionLineItem.objects.filter(transaction=transaction)

        serializer = TransactionSerializer(instance=transaction)
        return serializer.data

    def update(self, transaction_id, transaction_line_items):
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.save()

        Group.objects.filter(
            pk=transaction.group_id,
        ).update(updated_date=timezone.now())

        for transaction_line_item in transaction_line_items:
            transaction_line_item_id = transaction_line_item.pop('transaction_line_item', None)
            TransactionLineItem.objects.filter(
                pk=transaction_line_item_id,
            ).update(**transaction_line_item)

        return self.get(transaction_id=transaction_id)


class UserTransactionService:
    def get(self, user_id):
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

        return transactions_dict
