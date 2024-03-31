from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Currency


class OnlinePaymentUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    currency = forms.ModelChoiceField(queryset=Currency.objects.all())
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
            currency = self.cleaned_data['currency']
            initial_balance = calculate_initial_balance()
            UserProfile.objects.create(
                user=user,
                currency=currency,
                balance=initial_balance,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email']
            )
        return user


def calculate_initial_balance():
    initial_balance = 1000
    return initial_balance
