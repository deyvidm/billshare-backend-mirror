import json

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app.transaction.serializers import TransactionOperationSerializer
from app.transaction_line_item.serializers import TransactionIDSerializer, UpdateTransactionLineItemSerializer
from app.transaction_line_item.services import TransactionLineItemService
from app.response.services import ResponseService


@method_decorator(csrf_exempt, name='dispatch')
class TransactionLineItemView(View):

    response_service = ResponseService()
    transaction_line_item_service = TransactionLineItemService()

    def put(self, request, transaction_id):
        try:
            body = json.loads(request.body)
        except ValueError as e:
            return self.response_service.json_decode_exception({'error': str(e)})

        valid_transaction_request = UpdateTransactionLineItemSerializer(data={
            'id': transaction_id,
            'resolve': body['resolved']
        })
        if valid_transaction_request.is_valid() is False:
            return self.response_service.invalid_id({'serializer error': valid_transaction_request.errors})

        transaction = self.transaction_line_item_service.update(transaction_id, body['resolved'])
        return self.response_service.success(self.transaction_line_item_service.model_to_dict(transaction))

    def post(self, request):
        try:
            body = json.loads(request.body)
        except ValueError as e:
            return self.response_service.json_decode_exception({'error': str(e)})

        valid_transaction_operation = TransactionOperationSerializer(data=body)
        if valid_transaction_operation.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_transaction_operation.errors})

        try:
            transaction = self.transaction_line_item_service.processTransactionOperation(body)
        except Exception as e:
            return self.response_service.service_exception({'error': str(e)})

        if transaction is None:
            return self.response_service.failure({'error': 'something went wrong'})

        return self.response_service.success(self.transaction_line_item_service.get(transaction.id))

    def get(self, request, transaction_id):
        valid_transaction_id = TransactionIDSerializer(data={
            'id': transaction_id
        })

        # return self.response_service.success({valid_transaction_id.is_valid(): valid_transaction_id.data})

        if valid_transaction_id.is_valid() is False:
            return self.response_service.invalid_id({'serializer error': valid_transaction_id.errors})

        return self.response_service.success(self.transaction_line_item_service.get(transaction_id))
