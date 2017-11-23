from functools import reduce
import datetime
from decimal import Decimal

from djmoney.money import Money
from django.utils import timezone
from django.db.models import Q

from app.user.models import User
from app.group.models import Group
from app.transaction.models import Transaction
from app.transaction.models import TransactionLineItem
from app.transaction.serializers import TransactionSerializer


class TransactionService:
    def to_dec(self, x):
        return Decimal("%.2lf" % x)

    def dec_add(self, x, y):
        return self.to_dec(x) + self.to_dec(y)

    def dec_sub(self, x, y):
        return self.to_dec(x) - self.to_dec(y)

    def equalize_transaction_line_items_list(self, transaction_line_item_queue, total):
        debt_total = reduce(lambda x, y: self.dec_add(x, y), [t['debt'] for t in transaction_line_item_queue])
        diff = self.dec_sub(debt_total, total)
        if diff != self.to_dec(0):
            adjustment = self.to_dec(0.01)
            if diff > self.to_dec(0):
                adjustment = self.to_dec(-1) * adjustment
            counter = 0
            while diff != self.to_dec(0):
                transaction_line_item_queue[counter]['debt'] = self.dec_add(transaction_line_item_queue[counter]['debt'], adjustment)
                diff = self.dec_add(diff, adjustment)
                counter += 1

        return transaction_line_item_queue

    def create_transaction_line_items(self, transaction_line_item_queue, currency_code):
        for t in transaction_line_item_queue:
            t['debt'] = Money(t['debt'], currency_code)
            TransactionLineItem.objects.create(**t)

    def create_transaction(self, creator_id, group_id, user_shares, total, currency_code, label, split_type):

        paid_total = reduce(lambda x, y: x + y, [t['paid'] for t in user_shares])
        owes_total = reduce(lambda x, y: x + y, [t['owes'] for t in user_shares])

        if split_type == "percent":
            if paid_total != total or owes_total != 100:
                # TODO Custom Exception
                return None
        elif split_type == "money":
            if paid_total != owes_total or owes_total != total:
                # TODO Custom Exception
                return None
        else:
            return None

        transaction = Transaction.objects.create(
            label=label,
            group_id=group_id,
            creator_id=creator_id,
            total=Money(total, currency_code),
            split_type=split_type,
        )

        paid_shares = [{'user': t['user'], 'share': t['paid']} for t in user_shares if t['paid']]
        owes_shares = [{'user': t['user'], 'share': t['owes']} for t in user_shares if t['owes']]
        if split_type == "percent":
            owes_shares = [{'user': t['user'], 'share': t['owes'] * total / 100} for t in user_shares if t['owes']]

        transaction_line_item_queue = []
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
            transaction_line_item_queue.append({
                'transaction': transaction,
                'group_id': group_id,
                'debtor_id': owes_pair['user'],
                'creditor_id': paid_pair['user'],
                'debt': debt,
                'resolved': resolved,
                'percentage': percentage
            })

        transaction_line_item_queue = self.equalize_transaction_line_items_list(transaction_line_item_queue, total)
        self.create_transaction_line_items(transaction_line_item_queue, currency_code)

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

        transactions_dict = sorted(transactions_dict, key=lambda t: t['updated_date'], reverse=True)
        return transactions_dict

    def get_summary(self, user_id, last_date=None, first_date=None):
        if not last_date:
            last_date = timezone.now()
        if not first_date:
            first_date = (last_date.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)

        transactions = Transaction.objects.filter(
            Q(created_date__range=[first_date, last_date]) &
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

        if isinstance(debtTotal, Money):
            debtTotal = float(debtTotal.amount)
        if isinstance(creditTotal, Money):
            creditTotal = float(creditTotal.amount)

        return {
            "total transactions": len(transactions),
            "credit": creditTotal,
            "debt": debtTotal,
            "first_date": first_date,
            "last_date": last_date
        }
