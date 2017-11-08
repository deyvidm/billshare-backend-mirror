from django.views import View

from app.currency.services import FixerCurrencyService
from app.response.services import ResponseService


class CurrencyCodesView(View):

    response_service = ResponseService()
    fixer_currency_service = FixerCurrencyService()

    def get(self, request):

        currency_codes = self.fixer_currency_service.get_currency_codes()

        if currency_codes:
            return self.response_service.success(currency_codes)

        return self.response_service.failure({'error': 'Could not provide currency codes'})


class CurrencyView(View):

    response_service = ResponseService()
    fixer_currency_service = FixerCurrencyService()

    def get(self, request):
        currency_codes = self.fixer_currency_service.get_currency_code_rates()

        if currency_codes:
            return self.response_service.success(currency_codes)

        return self.response_service.failure({'error': 'Could not provide currency codes'})
