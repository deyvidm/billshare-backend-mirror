from django.db import models


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
    created_date = models.DateField(
        auto_now_add=True
    )
