import json

from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app.bill.serializers import BillSerializer
from app.response.services import ResponseService
from app.transaction.serializers import TransactionSerializer


@method_decorator(csrf_exempt, name='dispatch')
class TranasactionView(View):

    response_service = ResponseService()

    def post(self, request):
        try:
            body = json.loads(request.body)
        except ValueError as e:
            return self.response_service.json_decode_exception({'error': str(e)})

        valid_bill = BillSerializer(data=body)
        if valid_bill.is_valid() is False:
            return self.response_service.invalid_id({'error': valid_bill.errors})

        return self.response_service.success({"good": ":)"})
