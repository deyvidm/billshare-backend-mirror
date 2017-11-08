import requests

from moneyed import CURRENCIES


class CurrencyService:
    def get_currency_codes(self):
        return sorted(list(CURRENCIES.keys()), key=str.lower)


class FixerCurrencyService:

    fixer_url = 'https://api.fixer.io/'
    base_currency = 'CAD'
    historical_date = 'latest'

    currency_service = CurrencyService()

    #
    # Service to call fixer.io to get foreign exchange rates
    #
    # @param base_currency      String currency code, e.g. 'USD'
    # @param historical_date    A simple Date in 'YYYY-MM-DD', e.g. '2017-11-03'
    #
    # Note: When writing the validator use: https://stackoverflow.com/a/16870699/5698848
    #
    def __init__(self, base_currency=None, historical_date=None):
        if base_currency:
            self.base_currency = base_currency

        if historical_date:
            self.historical_date = historical_date

    def get_currency_code_rates(self, base_currency=None):
        base_currency = base_currency or self.base_currency

        response = requests.get(self.fixer_url + self.historical_date + '?' + 'base=' + base_currency)

        if response.status_code == 200:
            currency_codes = response.json().get('rates', None)

            if currency_codes:
                currency_codes[base_currency] = 1.0
                accepted_currency_codes = self.currency_service.get_currency_codes()

                return {currency_code: currency_codes[currency_code] for currency_code in accepted_currency_codes if currency_code in currency_codes}

        return None

    def get_currency_codes(self, base_currency=None):
        currency_codes = self.get_currency_code_rates(base_currency)

        if currency_codes:
            return list(currency_codes)

        return None
