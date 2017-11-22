from django.core.exceptions import ObjectDoesNotExist
from django.views import View

from app.auth.services import AuthService
from app.group.services import UserGroupService
from app.response.services import ResponseService
from app.transaction.services import UserTransactionService
from app.transaction.serializers import DateRangeSerializer

from app.user.serializers import UserIdSerializer
from app.user.services import UserService


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
        valid_group = UserIdSerializer(data={
            'id': user_id
        })

        if valid_group.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_group.errors})

        try:
            transactions = self.user_transaction_service.get(user_id)
        except Exception as e:
            return self.response_service.service_exception({'error': str(e)})

        return self.response_service.success(transactions)


class UserGroupsView(View):

    response_service = ResponseService()
    user_group_service = UserGroupService()

    def get(self, request, user_id):

        valid_user = UserIdSerializer(data={
            'id': user_id,
        })

        if valid_user.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_user.errors})

        try:
            groups = self.user_group_service.get(user_id)
        except ObjectDoesNotExist as e:
            return self.response_service.service_exception({'error': str(e)})

        return self.response_service.success(groups)


class UserTransactionsSummaryView(View):

    response_service = ResponseService()
    user_transaction_service = UserTransactionService()

    def get(self, request, user_id):

        valid_user = UserIdSerializer(data={'id': user_id})
        if valid_user.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_user.errors})

        valid_range = DateRangeSerializer(data=request.GET)
        if valid_range.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_range.errors})

        try:
            valid_range.validate_date_range(request.GET)
            summary = self.user_transaction_service.get_summary(
                user_id,
                request.GET["date_start"],
                request.GET["date_end"]
            )
        except Exception as e:
            return self.response_service.service_exception({'error': str(e)})

        return self.response_service.success(summary)
