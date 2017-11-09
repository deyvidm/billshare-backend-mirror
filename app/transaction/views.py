import json

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app.transaction.serializers import TransactionCreateSerializer
from app.transaction.serializers import TransactionIdSerializer, TransactionUpdateSerializer
from app.transaction.services import TransactionService
from app.response.services import ResponseService


@method_decorator(csrf_exempt, name='dispatch')
class TransactionView(View):

    response_service = ResponseService()
    transaction_service = TransactionService()

    def put(self, request):
        try:
            request_data = json.loads(request.body)
        except ValueError as e:
            return self.response_service.json_decode_exception({'error': str(e)})

        valid_transaction_request = TransactionUpdateSerializer(data=request_data)

        if valid_transaction_request.is_valid() is False:
            return self.response_service.invalid_id({'serializer error': valid_transaction_request.errors})

        transaction = self.transaction_service.update(
            transaction_id=request_data['transaction'],
            transaction_line_items=request_data['transaction_line_items'],
        )

        return self.response_service.success(transaction)

    def post(self, request):
        try:
            request_data = json.loads(request.body)
        except ValueError as e:
            return self.response_service.json_decode_exception({'error': str(e)})

        valid_transaction_create = TransactionCreateSerializer(data=request_data)
        if valid_transaction_create.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_transaction_create.errors})

        try:
            transaction = self.transaction_service.createTransaction(
                creator_id=request_data['creator'],
                group_id=request_data['group'],
                total=request_data['total'],
                currency_code=request_data['currency_code'],
                label=request_data['label'],
                user_shares=request_data['user_shares'],
                split_type=request_data['split_type']
            )
        except Exception as e:
            return self.response_service.service_exception({'error': str(e)})

        if transaction is None:
            return self.response_service.failure({'error': 'Could not process the Transaction'})

        return self.response_service.success(transaction)

    def get(self, request, transaction_id):
        valid_transaction_id = TransactionIdSerializer(data={
            'id': transaction_id
        })

        if valid_transaction_id.is_valid() is False:
            return self.response_service.invalid_id({'serializer error': valid_transaction_id.errors})

        return self.response_service.success(self.transaction_service.get(transaction_id))
