from rest_framework import generics
from rest_framework.response import Response
from register.currencies import CurrencyRate
from .serializers import ConversionSerializer


class ConvertCurrencyView(generics.GenericAPIView):
    serializer_class = ConversionSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        currency1 = serializer.validated_data['currency1']
        currency2 = serializer.validated_data['currency2']
        amount_of_currency1 = serializer.validated_data['amount_of_currency1']

        currency_rate = CurrencyRate()
        conversion_rate = currency_rate.get_rate(currency1, currency2)
        amount_of_currency2 = amount_of_currency1 * conversion_rate
        return Response({'result': amount_of_currency2})
