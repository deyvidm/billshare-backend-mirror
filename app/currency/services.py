from moneyed import CURRENCIES


class CurrencyService:
    def get_currency_codes(self):
        return sorted(list(CURRENCIES.keys()), key=str.lower)
