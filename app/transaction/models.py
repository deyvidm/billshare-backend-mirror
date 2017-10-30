from django.db import models

from djmoney.models.fields import MoneyField


class Transaction(models.Model):
    label = models.TextField(
        max_length=255,
        blank=False,
        null=False,
    )
    group = models.ForeignKey(
        'group.Group'
    )
    creator = models.ForeignKey(
        'user.User'
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        auto_now=True
    )


class TransactionLineItem(models.Model):
    label = models.CharField(
        max_length=255,
        blank=True,
    )
    transaction = models.ForeignKey(
        'transaction.Transaction',
        related_name='transaction_line_items',
    )
    group = models.ForeignKey(
        'group.Group',
    )
    debt = MoneyField(
        max_digits=10,
        decimal_places=2,
    )
    debtor = models.ForeignKey(
        'user.User',
        related_name='debtors',
    )
    creditor = models.ForeignKey(
        'user.User',
        related_name='creditors',
    )
    resolved = models.BooleanField()
