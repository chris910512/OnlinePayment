class Currency:
    # Currency rates are based on 16th April 2024
    GBP = {'code': 'GBP', 'name': 'British Pound', 'GBP/USD': 1.25, 'GBP/EUR': 1.17}
    USD = {'code': 'USD', 'name': 'US Dollar', 'USD/EUR': 0.94, 'USD/GBP': 0.80}
    EUR = {'code': 'EUR', 'name': 'Euro', 'EUR/GBP': 0.85, 'EUR/USD': 1.06}

    @staticmethod
    def get_all_currencies():
        return [Currency.GBP, Currency.USD, Currency.EUR]


class CurrencyRate:
    def __init__(self):
        self.currencies = Currency.get_all_currencies()
        self.currency_rates = self.calculate_currency_rates()

    def calculate_currency_rates(self):
        currency_rates = {}
        for base_currency in self.currencies:
            for target_currency in self.currencies:
                if base_currency['code'] != target_currency['code']:
                    rate = base_currency[f"{base_currency['code']}/{target_currency['code']}"]
                    currency_rates[f"{base_currency['code']}/{target_currency['code']}"] = rate
        return currency_rates

    def get_rate(self, base_currency_code, target_currency_code):
        return self.currency_rates[f"{base_currency_code}/{target_currency_code}"]
