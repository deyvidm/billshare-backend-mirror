from django.views import View
from django.http import JsonResponse

from app.user.serializers import UserIdSerializer
from app.user.service import UserService
from app.response.service import ResponseService


class UserView(View):

    def get(self, request, user_id):

        user_service = UserService()
        response_service = ResponseService()

        valid_user = UserIdSerializer(data={
            'id': user_id
        })

        if valid_user.is_valid() is False:
            return response_service.invalid_id({'error': valid_user.errors})

        try:
            user = user_service.get(user_id)
        except Exception as e:
            return response_service.service_exception({'error': str(e)})

        return response_service.success(user)
