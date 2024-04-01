class Currency:
    GBP = {'code': 'GBP', 'name': 'British Pound', 'conversion_rate_to_gbp': 1}
    USD = {'code': 'USD', 'name': 'US Dollar', 'conversion_rate_to_gbp': 1.39}  # Update this with the current rate
    EUR = {'code': 'EUR', 'name': 'Euro', 'conversion_rate_to_gbp': 1.17}  # Update this with the current rate

    @staticmethod
    def get_all_currencies():
        return [Currency.GBP, Currency.USD, Currency.EUR]

    @staticmethod
    def get_conversion_rates():
        return {
            'GBP': Currency.GBP['conversion_rate_to_gbp'],
            'USD': Currency.USD['conversion_rate_to_gbp'],
            'EUR': Currency.EUR['conversion_rate_to_gbp'],
        }
