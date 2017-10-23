import json

from django.forms import model_to_dict
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from djmoney.money import Money


from app.bill.serializers import BillSerializer
from app.transaction.serializers import TransactionIDSerializer
from app.transaction.services import TransactionService
from app.response.services import ResponseService


@method_decorator(csrf_exempt, name='dispatch')
class TranasactionView(View):

    response_service = ResponseService()
    transaction_service = TransactionService()

    def post(self, request):
        try:
            body = json.loads(request.body)
        except ValueError as e:
            return self.response_service.json_decode_exception({'error': str(e)})

        valid_bill = BillSerializer(data=body)
        if valid_bill.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_bill.errors})

        try:
            result = self.transaction_service.crombobulate(body)
        except Exception as e:
            return self.response_service.service_exception({'error': str(e)})

        if result is not True:
            return self.response_service.failure({'error': 'something went wrong'})

        return self.response_service.success(result)

    def get(self, request, transaction_id):

        # return self.response_service.success(model_to_dict(Money(10, "CAD")))

        valid_transaction_id = TransactionIDSerializer(data={
            'id': transaction_id
        })
        if valid_transaction_id.is_valid() is False:
            return self.response_service.invalid_id({'serializer error': valid_transaction_id.errors})

        return self.response_service.success(self.transaction_service.get(transaction_id))
