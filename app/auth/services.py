from django.contrib.auth import authenticate

from app.user.services import UserService


class AuthService():

    def authenticate(self, email, password):
        user_service = UserService()

        user = authenticate(email=email, password=password)

        if user is None:
            return None

        return user_service.get(user.pk)
