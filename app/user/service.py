from app.user.models import User


class UserService():

    def get(self, user_id):
        return User.objects.get_user({'pk': user_id})
