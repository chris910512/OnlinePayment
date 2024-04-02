from _decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Notification


@transaction.atomic
def make_payment(request):
    sender = request.user
    recipient_username = request.POST.get('recipient')
    amount = Decimal(request.POST.get('amount'))

    recipient = User.objects.get(username=recipient_username)

    if sender.userprofile.balance >= amount:
        sender.userprofile.balance -= amount
        recipient.userprofile.balance += amount

        sender.userprofile.save()
        recipient.userprofile.save()

        Notification.objects.create(sender=sender, recipient=recipient, amount=amount)

        messages.success(request, 'Payment was successful.')
        return redirect(reverse('user_list'))
    else:
        messages.error(request, 'Payment failed. Not enough balance.')
        return redirect(reverse('user_list'))


@login_required
def notifications(request):
    notifications = Notification.objects.filter(Q(sender=request.user) | Q(recipient=request.user))
    return render(request, 'notifications.html', {'notifications': notifications})
