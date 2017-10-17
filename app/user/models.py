from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):

    email = models.EmailField(
        max_length=255,
        unique=True,
        db_index=True,
        blank=False,
        null=False,
    )
    first_name = models.TextField(
        max_length=255,
        blank=False,
        null=False,
    )
    last_name = models.TextField(
        max_length=255,
        blank=False,
        null=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name'
    ]
