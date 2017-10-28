from django.db import models

from djmoney.models.fields import MoneyField


class TransactionLineItem(models.Model):
    label = models.CharField(
        max_length=255,
        blank=True,
    )
    transaction = models.ForeignKey(
        "transaction.Transaction"
    )
    group = models.ForeignKey(
        "group.Group"
    )
    debt = MoneyField(
        max_digits=10,
        decimal_places=2
    )
    payee = models.ForeignKey(
        'user.User',
        related_name='incoming_pays'
    )
    payer = models.ForeignKey(
        'user.User',
        related_name='outgoing_pays'
    )
    resolved = models.BooleanField()
