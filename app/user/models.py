from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractBaseUser):

    email = models.EmailField(
        _('email address'),
        max_length=255,
        unique=True,
        db_index=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
