from django.contrib.auth import authenticate, login, logout

from app.user.services import UserService


class AuthService():

    def authenticate(self, request, email, password):
        user_service = UserService()

        user = authenticate(email=email, password=password)

        if user is None:
            return None

        user.second_last_login = user.last_login

        login(request, user)

        return user_service.get(user.pk)

    def unauthenticate(self, request):
        logout(request)

    def is_authenticated(self, request):
        return request.user.is_authenticated

    def create_user(self, email, password, first_name, last_name):
        user_service = UserService()
        user = user_service.create(email=email, password=password, first_name=first_name, last_name=last_name)

        return user_service.get(user.pk)
