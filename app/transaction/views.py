import json

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app.bill.serializers import BillSerializer
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

        result = self.transaction_service.crombobulate(body)
        return self.response_service.success(result)

        if self.transaction_service.crombobulate(body) is not True:
            return self.response_service.failure({'error': 'something went wrong'})

        return self.response_service.success(body)
