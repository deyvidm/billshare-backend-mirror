from functools import reduce

from djmoney.money import Money

from app.bill.models import Bill
from app.group.models import Group
from app.transaction.models import Transaction
from app.user.models import User


class TransactionService:
    def crombobulate(self, entry):
        if len(entry['transactions']) == 0:
            return None

        paid_total = reduce(lambda x, y: x + y, [t['paid'] for t in entry['transactions']])
        owes_total = reduce(lambda x, y: x + y, [t['owes'] for t in entry['transactions']])

        # TODO it's possible that entry['total'] is not an int...
        if paid_total != owes_total or owes_total != entry['total']:
            # TODO should this be an exception?
            return None

        Money(0, entry['currency_code'])

        overpaid = []
        underpaid = []

        for transaction in entry['transactions']:
            node = {
                'user_id': transaction['payer'],
                'zerosum': transaction['paid'] - transaction['owes']
            }

            if node['zerosum'] < 0:
                underpaid.append(node)
            if node['zerosum'] > 0:
                overpaid.append(node)

        q = []
        log = []
        bill = self.createBill(entry['label'], entry['group'], entry['creator'])

        while len(overpaid) > 0:
            overpaid = sorted(overpaid, key=lambda t: t['zerosum'])
            underpaid = sorted(underpaid, key=lambda t: t['zerosum'], reverse=True)

            give_to = overpaid.pop()
            take_from = underpaid.pop()

            # log.append(str(give_to['zerosum']) + " vs " + str(take_from['zerosum']))

            if give_to['zerosum'] + take_from['zerosum'] >= 0:
                # log.append("in if")
                give_to['zerosum'] += take_from['zerosum']
                owed = abs(take_from['zerosum'])
                take_from['zerosum'] = 0
            else:
                # log.append("in else")
                take_from['zerosum'] += give_to['zerosum']
                owed = give_to['zerosum']
                give_to['zerosum'] = 0

            self.createTransaction(bill, entry['group'], take_from['user_id'], give_to['user_id'], owed, entry['currency_code'])

            if give_to['zerosum'] != 0:
                overpaid.append(give_to)

            if take_from['zerosum'] != 0:
                underpaid.append(take_from)

        return True

    def createBill(self, label, group_id, creator_id):
        return Bill.objects.create(
            label=label,
            group=Group.objects.get(id=group_id),
            creator=User.objects.get(id=creator_id),
        )

    def createTransaction(self, bill, group_id, payer_id, payee_id, amount, currency):

        payer = User.objects.get(id=payer_id)
        payee = User.objects.get(id=payee_id)
        return Transaction.objects.create(
            bill=bill,
            group=Group.objects.get(id=group_id),
            payer=payer,
            payee=payee,
            debt=Money(amount, currency)
        )
