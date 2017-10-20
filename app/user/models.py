from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.forms import model_to_dict


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def get_user(self, params):
        user = self.get(**params)

        return model_to_dict(
            user,
            fields=None,
            exclude=[
                'password',
            ],
        )


class User(AbstractBaseUser):
    objects = UserManager()

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
