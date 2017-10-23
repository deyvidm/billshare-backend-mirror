from django.db import models

from djmoney.models.fields import MoneyField


class Transaction(models.Model):
    label = models.TextField(
        max_length=255,
        blank=False,
        null=False,
    )
    bill = models.ForeignKey(
        "bill.Bill"
    )
    group = models.ForeignKey(
        "group.Group"
    )
    debt = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='CAD'
    )
    payee = models.ForeignKey(
        'user.User',
        related_name='incoming_pays'
    )
    payer = models.ForeignKey(
        'user.User',
        related_name='outgoing_pays'
    )
    resolved = models.BooleanField(
        default=False
    )
