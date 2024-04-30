from rest_framework import serializers


class ConversionSerializer(serializers.Serializer):
    currency1 = serializers.CharField(max_length=3)
    currency2 = serializers.CharField(max_length=3)
    amount_of_currency1 = serializers.IntegerField()
