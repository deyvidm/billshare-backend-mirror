from functools import reduce

from django.forms import model_to_dict
from djmoney.money import Money

from app.group.models import Group

from app.transaction.models import Transaction
from app.transaction.models import TransactionLineItem
from app.transaction.serializers import TransactionSerializer

from app.user.models import User


class TransactionService:
    def processTransactionCreate(self, creator_id, group_id, user_shares, total, currency_code, label):

        paid_total = reduce(lambda x, y: x + y, [t['paid'] for t in user_shares])
        owes_total = reduce(lambda x, y: x + y, [t['owes'] for t in user_shares])

        if paid_total != owes_total or owes_total != total:
            # TODO should this be an exception?
            return None

        Money(0, currency_code)

        overpaid = []
        underpaid = []

        for transaction_line_item in user_shares:
            node = {
                'user_id': transaction_line_item['user'],
                'zerosum': transaction_line_item['paid'] - transaction_line_item['owes']
            }

            if node['zerosum'] < 0:
                underpaid.append(node)
            if node['zerosum'] > 0:
                overpaid.append(node)

        transaction = self.createTransaction(label, group_id, creator_id)

        while len(overpaid) > 0:
            overpaid = sorted(overpaid, key=lambda t: t['zerosum'])
            underpaid = sorted(underpaid, key=lambda t: t['zerosum'], reverse=True)

            give_to = overpaid.pop()
            take_from = underpaid.pop()

            if give_to['zerosum'] + take_from['zerosum'] >= 0:
                give_to['zerosum'] += take_from['zerosum']
                owed = abs(take_from['zerosum'])
                take_from['zerosum'] = 0
            else:
                take_from['zerosum'] += give_to['zerosum']
                owed = give_to['zerosum']
                give_to['zerosum'] = 0

            self.createTransactionLineItem(transaction, group_id, take_from['user_id'], give_to['user_id'], owed, currency_code, False)

            if give_to['zerosum'] != 0:
                overpaid.append(give_to)

            if take_from['zerosum'] != 0:
                underpaid.append(take_from)

        return transaction

    def createTransaction(self, label, group_id, creator_id):
        return Transaction.objects.create(
            label=label,
            group=Group.objects.get(id=group_id),
            creator=User.objects.get(id=creator_id),
        )

    def createTransactionLineItem(self, transaction, group_id, debtor_id, creditor_id, amount, currency, resolved):

        transaction_line_item = TransactionLineItem(
            transaction=transaction,
            group=Group.objects.get(id=group_id),
            debt=Money(amount, currency),
            resolved=resolved
        )

        transaction_line_item.debtor_id = debtor_id
        transaction_line_item.creditor_id = creditor_id
        transaction_line_item.save()

        return transaction_line_item

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
