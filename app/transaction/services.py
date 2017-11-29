import datetime
from decimal import Decimal
from functools import reduce

from djmoney.money import Money
from django.utils import timezone
from django.db.models import Q

from app.currency.services import FixerCurrencyService
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

    def dec_multiply(self, x, y):
        return self.to_dec(x) * self.to_dec(y)

    def normalize_amount(self, money_obj):
        normalizing_currency = "CAD"
        fixer_currency_service = FixerCurrencyService()

        if not isinstance(money_obj, Money):
            raise Exception("Function expects Money object -- received " + money_obj.__class__.__name__)

        if money_obj.currency == normalizing_currency:
            return money_obj

        rates = fixer_currency_service.get_currency_code_rates(money_obj.currency.code)

        return Money(
            self.dec_multiply(money_obj.amount, rates.get(normalizing_currency)),
            normalizing_currency
        )

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

    def sum_debt_credit_from_line_items(self, user_id, line_items):
        debt_total = 0
        credit_total = 0

        user = User.objects.get(pk=user_id)
        for line_item in line_items:
            if line_item.debtor == user:
                debt_total += line_item.debt
            elif line_item.creditor == user:
                credit_total += line_item.debt

        if isinstance(debt_total, Money):
            debt_total = float(debt_total.amount)
        if isinstance(credit_total, Money):
            credit_total = float(credit_total.amount)

        return [debt_total, credit_total]

    def resolve_balance_from_line_items(self, user_id, line_items):
        debt_total, credit_total = self.sum_debt_credit_from_line_items(user_id, line_items)
        return credit_total - debt_total

    def get_transaction_line_items(self, user_id, group_id, resolved):
        debtor = Q(debtor=User.objects.get(pk=user_id))
        creditor = Q(creditor=User.objects.get(pk=user_id))
        filter_bits = debtor | creditor

        if group_id is not None:
            filter_bits = filter_bits & (Q(group=Group.objects.get(pk=group_id)))
        if resolved is not None:
            filter_bits = filter_bits & (Q(resolved=resolved))

        return TransactionLineItem.objects.filter(filter_bits)

    def get(self, user_id, group_id, resolved):
        transaction_service = TransactionService()

        transaction_line_items = self.get_transaction_line_items(user_id, group_id, resolved)
        transaction_ids = sorted(set([t.transaction.id for t in transaction_line_items]))

        transactions_dict = []
        for transaction_id in transaction_ids:
            transaction = transaction_service.get(transaction_id)
            transactions_dict.append(transaction)

        transactions_dict = sorted(transactions_dict, key=lambda t: t['updated_date'], reverse=True)
        return transactions_dict

    def get_transactions_in_range(self, user_id, start_date, end_date):
        return Transaction.objects.filter(
            Q(created_date__range=[start_date, end_date]) &
            (
                Q(transaction_line_items__debtor=user_id) |
                Q(transaction_line_items__creditor=user_id)
            )
        ).distinct()

    def get_summary(self, user_id, start_date=None, end_date=None):
        transaction_service = TransactionService()

        if not end_date:
            end_date = timezone.now()
        if not start_date:
            start_date = (end_date.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)

        transactions = self.get_transactions_in_range(user_id, start_date, end_date)

        debtTotal = 0
        creditTotal = 0
        user = User.objects.get(pk=user_id)
        transaction_ids = sorted(set([t.id for t in transactions.all()]))
        for transaction_id in transaction_ids:
            transaction = Transaction.objects.get(pk=transaction_id)
            for line_item in transaction.transaction_line_items.all():
                if line_item.debtor == user and line_item.creditor == user:
                    continue
                if line_item.debtor == user:
                    debtTotal += transaction_service.normalize_amount(line_item.debt)
                elif line_item.creditor == user:
                    creditTotal += transaction_service.normalize_amount(line_item.debt)

        if isinstance(debtTotal, Money):
            debtTotal = float(debtTotal.amount)
        if isinstance(creditTotal, Money):
            creditTotal = float(creditTotal.amount)

        return {
            "total_transactions": len(transactions),
            "credit": creditTotal,
            "debt": debtTotal,
            "date_start": start_date,
            "date_end": end_date
        }
