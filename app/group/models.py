from django.db import models


class Group(models.Model):
    label = models.TextField(
        max_length=255,
        blank=False,
        null=False,
    )

    creator = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE
    )


class GroupUser(models.Model):
    group_id = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE
    )

    user_id = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE
    )
