from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .currencies import Currency, CurrencyRate
from .models import UserProfile


class OnlinePaymentUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    currency = forms.ChoiceField(choices=[(currency['code'], currency['code']) for currency in Currency.get_all_currencies()])
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'currency']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            currency_code = self.cleaned_data['currency']
            initial_balance = calculate_initial_balance(currency_code)
            UserProfile.objects.create(
                user=user,
                currency=currency_code,
                balance=initial_balance,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email']
            )
        return user


def calculate_initial_balance(currency_code):
    base_amount_gbp = 1000
    if currency_code == 'GBP':
        return base_amount_gbp
    else:
        currency_rate = CurrencyRate()
        conversion_rate = currency_rate.get_rate('GBP', currency_code)
        return base_amount_gbp * conversion_rate

