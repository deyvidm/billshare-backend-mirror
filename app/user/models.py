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

    def update_user(self, query_params, update_params):
        excluded_fields = [
            'password',
        ]

        user = self.get(**query_params)

        for key, value in update_params.items():
            if key not in excluded_fields:
                setattr(user, key, value)

        if 'password' in update_params:
            user.set_password(update_params['password'])

        user.save()

    def delete_user(self, query_params):
        user = self.get(**query_params)
        user.delete()


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
