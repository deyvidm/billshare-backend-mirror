from django.core.exceptions import ObjectDoesNotExist

from app.user.models import User


class UserService:

    def get(self, user_id):
        return User.objects.get_user({'pk': user_id})

    def create(self, email, password, first_name, last_name):
        return User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)

    def update(self, user_id, updated_fields):
        return User.objects.update_user({'pk': user_id}, updated_fields)

    def delete(self, user_id):
        return User.objects.delete_user({'pk': user_id})

    def email_exists(self, email):

        try:
            User.objects.get_user({'email': email})
        except ObjectDoesNotExist:
            return False

        return True
