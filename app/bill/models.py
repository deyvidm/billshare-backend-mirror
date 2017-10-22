from django.db import models


class Bill(models.Model):
    label = models.TextField(
        max_length=255,
        blank=False,
        null=False,
    )

    group = models.ForeignKey()
