import sys
from functools import reduce

from djmoney.money import Money

from app.transaction.models import Transaction
from app.transaction.models import TransactionLineItem
from app.transaction.serializers import TransactionSerializer


class TransactionService:
    def createTransaction(self, creator_id, group_id, user_shares, total, currency_code, label, split_type):

        paid_total = reduce(lambda x, y: x + y, [t['paid'] for t in user_shares])
        owes_total = reduce(lambda x, y: x + y, [t['owes'] for t in user_shares])

        if split_type == "percent":
            if paid_total != owes_total or owes_total != 100:
                # TODO Custom Exception
                return None
        elif split_type == "dollar":
            if paid_total != owes_total or owes_total != total:
                # TODO Custom Exception
                return None
        else:
            return None

        transaction = Transaction.objects.create(
            label=label,
            group_id=group_id,
            creator_id=creator_id,
            total=Money(total, currency_code)
        )

        print("test", sys.stderr)
        if split_type == "dollar":
            paid_shares = [{'user': t['user'], 'share': t['paid']} for t in user_shares if t['paid']]
            owes_shares = [{'user': t['user'], 'share': t['owes']} for t in user_shares if t['owes']]
        if split_type == "percent":
            paid_shares = [{'user': t['user'], 'share': t['paid'] * total / 100} for t in user_shares if t['paid']]
            owes_shares = [{'user': t['user'], 'share': t['owes'] * total / 100} for t in user_shares if t['owes']]

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

            percentage = debt / total * 100
            TransactionLineItem.objects.create(
                transaction=transaction,
                group_id=group_id,
                debtor_id=owes_pair['user'],
                creditor_id=paid_pair['user'],
                debt=Money(debt, currency_code),
                resolved=resolved,
                percentage=percentage
            )

        return self.get(transaction_id=transaction.id)

    def get(self, transaction_id):
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.transaction_line_items = TransactionLineItem.objects.filter(transaction=transaction)

        serializer = TransactionSerializer(instance=transaction)
        return serializer.data

    def update(self, transaction_id, transaction_line_items):
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.save()

        for transaction_line_item in transaction_line_items:
            transaction_line_item_id = transaction_line_item.pop('transaction_line_item', None)
            TransactionLineItem.objects.filter(
                pk=transaction_line_item_id,
            ).update(**transaction_line_item)

        return self.get(transaction_id=transaction_id)
