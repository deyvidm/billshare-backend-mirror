from django.db import models


class Group(models.Model):
    label = models.TextField(
        max_length=255,
        blank=False,
        null=False,
    )

    creator = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
    )

    updated_date = models.DateTimeField(
        auto_now_add=True,
    )


class GroupUser(models.Model):
    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        related_name='_group_users',
    )

    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='_group_users',
    )
