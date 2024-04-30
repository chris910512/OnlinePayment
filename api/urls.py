from django.urls import path
from .views import ConvertCurrencyView

urlpatterns = [
    path('conversion/<str:currency1>/<str:currency2>/<int:amount_of_currency1>', ConvertCurrencyView.as_view(), name='convert_currency'),
]
