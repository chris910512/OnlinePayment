import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .currencies import CurrencyRate
from .forms import OnlinePaymentUserCreationForm
from .models import UserProfile

home_url = '/register/user-list'


def user_list(request):
    user_profiles = UserProfile.objects.all().values('user__username', 'first_name', 'last_name', 'currency')
    if request.user.is_authenticated:
        current_user_profile = UserProfile.objects.get(user=request.user)
    else:
        current_user_profile = None
    return render(request, 'user_list.html',{
        'users': user_profiles,
        'current_user_profile': current_user_profile
    })


def logout_view(request):
    logout(request)
    return redirect('%s' % home_url)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/register/user-list')
        else:
            pass
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'login_user': form})


def signup_view(request):
    if request.method == 'POST':
        form = OnlinePaymentUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/register/user-list')
    else:
        form = OnlinePaymentUserCreationForm()
        currency_rate = CurrencyRate()
        conversion_rates = {
            'GBP': 1,  # Base currency
            'USD': currency_rate.get_rate('GBP', 'USD'),
            'EUR': currency_rate.get_rate('GBP', 'EUR')
        }
        return render(request, 'signup.html', {'form': form, 'conversion_rates': json.dumps(conversion_rates)})
