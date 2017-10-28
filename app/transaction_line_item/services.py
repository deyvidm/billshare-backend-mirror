from functools import reduce

from django.forms import model_to_dict
from djmoney.money import Money

from app.transaction.models import Transaction
from app.group.models import Group
from app.transaction_line_item.models import TransactionLineItem
from app.user.models import User


class TransactionLineItemService:
    def processTransactionOperation(self, entry):
        if not entry['transaction_line_items']:
            return None

        paid_total = reduce(lambda x, y: x + y, [t['paid'] for t in entry['transaction_line_items']])
        owes_total = reduce(lambda x, y: x + y, [t['owes'] for t in entry['transaction_line_items']])

        if paid_total != owes_total or owes_total != entry['total']:
            # TODO should this be an exception?
            return None

        Money(0, entry['currency_code'])

        overpaid = []
        underpaid = []

        for transaction_line_item in entry['transaction_line_items']:
            node = {
                'user_id': transaction_line_item['payer'],
                'zerosum': transaction_line_item['paid'] - transaction_line_item['owes']
            }

            if node['zerosum'] < 0:
                underpaid.append(node)
            if node['zerosum'] > 0:
                overpaid.append(node)

        transaction = self.createTransaction(entry['label'], entry['group'], entry['creator'])

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

            self.createTransactionLineItem(transaction, entry['group'], take_from['user_id'], give_to['user_id'], owed, entry['currency_code'], False)

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

    def createTransactionLineItem(self, transaction, group_id, payer_id, payee_id, amount, currency, resolved):

        payer = User.objects.get(id=payer_id)
        payee = User.objects.get(id=payee_id)
        return TransactionLineItem.objects.create(
            transaction=transaction,
            group=Group.objects.get(id=group_id),
            payer=payer,
            payee=payee,
            debt=Money(amount, currency),
            resolved=resolved
        )

    def get(self, transaction_id):
        transaction = Transaction.objects.get(id=transaction_id)
        transaction_line_items = TransactionLineItem.objects.filter(transaction=transaction)

        transaction_dict = {
            "transaction": model_to_dict(transaction),
            'transaction_line_items': []
        }
        for t in transaction_line_items:
            transaction_dict['transaction_line_items'].append(self.model_to_dict(t))

        return transaction_dict

    # TODO Guido pls forgive me
    def model_to_dict(self, transaction_line_item):
        return {
            "id": transaction_line_item.id,
            "label": transaction_line_item.label,
            "transaction": transaction_line_item.transaction.id,
            "group": transaction_line_item.group.id,
            "debt": {
                "amount": transaction_line_item.debt.amount,
                "currency": transaction_line_item.debt.currency.code
            },
            "payee": transaction_line_item.payee.id,
            "payer": transaction_line_item.payer.id,
            "resolved": transaction_line_item.resolved,
        }

    def update(self, transaction_line_item_id, resolved):
        transaction_line_item = TransactionLineItem.objects.get(id=transaction_line_item_id)
        transaction_line_item.resolved = resolved
        transaction_line_item.save()
        return transaction_line_item
