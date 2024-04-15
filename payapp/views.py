from _decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Notification, Transaction, PaymentRequest


@transaction.atomic
def make_payment(request):
    sender = request.user
    recipient_username = request.POST.get('recipient')
    amount = Decimal(request.POST.get('amount'))

    recipient = User.objects.get(username=recipient_username)

    if sender.userprofile.balance >= amount:
        make_transaction(amount, recipient, sender)

        messages.success(request, 'Payment was successful.')
        return redirect(reverse('user_list'))
    else:
        messages.error(request, 'Payment failed. Not enough balance.')
        return redirect(reverse('user_list'))


def make_transaction(amount, recipient, sender):
    sender.userprofile.balance -= amount
    recipient.userprofile.balance += amount
    sender.userprofile.save()
    recipient.userprofile.save()
    Notification.objects.create(sender=sender, recipient=recipient, amount=amount)
    Transaction.objects.create(sender=sender.userprofile, recipient=recipient.userprofile, amount=amount)


def request_payment(request):
    if request.method == 'POST':
        sender = request.user
        recipient_username = request.POST.get('recipient')
        recipient = User.objects.get(username=recipient_username)
        amount = Decimal(request.POST.get('amount'))

        PaymentRequest.objects.create(sender=sender.userprofile, recipient=recipient.userprofile, amount=amount)

        messages.success(request, 'Payment request was successful.')
        return redirect(reverse('user_list'))
    else:
        return render(request, 'request_payment.html')


@login_required
def notifications(request):
    received_payments = Transaction.objects.filter(recipient=request.user.userprofile)
    sent_payments = Transaction.objects.filter(sender=request.user.userprofile)
    payment_requests = PaymentRequest.objects.filter(recipient=request.user.userprofile)

    return render(request, 'notifications.html', {
        'received_payments': received_payments,
        'sent_payments': sent_payments,
        'payment_requests': payment_requests
    })


@transaction.atomic
def accept_payment_request(request, request_id):
    payment_request = get_object_or_404(PaymentRequest, id=request_id)

    sender = payment_request.sender.user
    recipient = payment_request.recipient.user
    amount = payment_request.amount

    if sender.userprofile.balance >= amount:
        make_transaction(amount, recipient, sender)

        payment_request.is_accepted = True
        payment_request.save()

        messages.success(request, 'Payment request accepted.')
    else:
        messages.error(request, 'Payment request could not be accepted.')

    return redirect(reverse('notifications'))


@transaction.atomic
def decline_payment_request(request, request_id):
    payment_request = get_object_or_404(PaymentRequest, id=request_id)

    if payment_request.recipient.user == request.user:
        payment_request.is_accepted = False
        payment_request.save()

        messages.success(request, 'Payment request declined.')
    else:
        messages.error(request, 'Payment request could not be declined.')

    return redirect(reverse('notifications'))
