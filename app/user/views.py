from django.views import View

from app.auth.services import AuthService
from app.user.serializers import UserIdSerializer
from app.user.services import UserService, UserTransactionService
from app.response.services import ResponseService


class UserView(View):

    def get(self, request, user_id):

        user_service = UserService()
        response_service = ResponseService()

        valid_user = UserIdSerializer(data={
            'user': user_id
        })

        if valid_user.is_valid() is False:
            return response_service.invalid_id({'error': valid_user.errors})

        try:
            user = user_service.get(user_id)
        except Exception as e:
            return response_service.service_exception({'error': str(e)})

        return response_service.success(user)


class GetUserIdView(View):

    def get(self, request):

        auth_service = AuthService()
        response_service = ResponseService()

        if auth_service.is_authenticated is False:
            return response_service.failure({'error': 'Not logged in.'})

        return response_service.success({'user': request.user.id})


class UserTransactionsView(View):

    response_service = ResponseService()
    user_transaction_service = UserTransactionService()

    def get(self, request, user_id):
        valid_group = UserIdSerializer(data={'user': user_id})
        if valid_group.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_group.errors})

        try:
            transactions = self.user_transaction_service.get(user_id)
        except Exception as e:
            return self.response_service.service_exception({'error': str(e)})

        return self.response_service.success(transactions)
