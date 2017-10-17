from django.views import View
from django.http import JsonResponse

from app.user.serializers import UserIdSerializer


class UserView(View):

    def get(self, request, user_id):

        valid_user = UserIdSerializer(data={
            'id': user_id
        })

        if valid_user.is_valid() is False:
            return JsonResponse(valid_user.errors)

        return JsonResponse({})
