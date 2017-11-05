from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app.currency.services import CurrencyService
from app.response.services import ResponseService


@method_decorator(csrf_exempt, name='dispatch')
class CurrencyCodesView(View):

    response_service = ResponseService()
    currency_service = CurrencyService()

    def get(self, request):
        return self.response_service.success(self.currency_service.get_currency_codes())
