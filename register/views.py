import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .currencies import Currency
from .forms import OnlinePaymentUserCreationForm
from .models import UserProfile

home_url = '/register/user-list'


def user_list(request):
    users = UserProfile.objects.all()
    return render(request, 'user_list.html', {'users': users})


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
        conversion_rates = Currency.get_conversion_rates()
        return render(request, 'signup.html', {'form': form, 'conversion_rates': json.dumps(conversion_rates)})
