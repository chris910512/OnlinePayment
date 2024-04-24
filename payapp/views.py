from _decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseNotAllowed
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from register.currencies import CurrencyRate
from timestamp_service.utils import get_timestamp
from .models import Notification, Transaction, PaymentRequest


@transaction.atomic
def make_payment(request):
    sender = request.user
    recipient_username = request.POST.get('recipient')
    amount = Decimal(request.POST.get('amount'))

    recipient = User.objects.get(username=recipient_username)

    if sender.userprofile.balance >= amount:
        recipient_currency, converted_amount = make_transaction(amount, recipient, sender)

        messages.success(request,
                         f'Payment was successful. \n{converted_amount} {recipient_currency} was sent to {recipient.username}.')
        return redirect(reverse('user_list'))
    else:
        messages.error(request, 'Payment failed. Not enough balance.')
        return redirect(reverse('user_list'))


def make_transaction(amount, recipient, sender):
    currency_rate = CurrencyRate()
    sender_currency = sender.userprofile.currency
    recipient_currency = recipient.userprofile.currency

    rate = Decimal(currency_rate.get_rate(sender_currency, recipient_currency))
    converted_amount = round(rate * amount, 2)

    # Transactions
    sender.userprofile.balance -= amount
    recipient.userprofile.balance += converted_amount
    sender.userprofile.save()
    recipient.userprofile.save()
    timestamp = get_timestamp()

    Notification.objects.create(sender=sender, recipient=recipient, amount=converted_amount, timestamp=timestamp)
    Transaction.objects.create(sender=sender.userprofile, recipient=recipient.userprofile, amount=converted_amount, timestamp=timestamp)

    return recipient_currency, converted_amount


def request_payment(request):
    if request.method == 'POST':
        sender = request.user
        recipient_username = request.POST.get('recipient')
        recipient = User.objects.get(username=recipient_username)
        amount = Decimal(request.POST.get('amount'))
        timestamp = get_timestamp()

        # Sender and Recipient are swapped in the PaymentRequest model
        PaymentRequest.objects.create(sender=recipient.userprofile, recipient=sender.userprofile, amount=amount, timestamp=timestamp)

        messages.success(request, 'Payment request was successful.')
        return redirect(reverse('user_list'))


@login_required
def notifications(request):
    received_payments = Transaction.objects.filter(recipient=request.user.userprofile)
    sent_payments = Transaction.objects.filter(sender=request.user.userprofile)
    payment_requests = PaymentRequest.objects.filter(sender=request.user.userprofile)
    user_currency = request.user.userprofile.currency

    return render(request, 'notifications.html', {
        'received_payments': received_payments,
        'sent_payments': sent_payments,
        'payment_requests': payment_requests,
        'user_currency': user_currency
    })


@transaction.atomic
def accept_payment_request(request, request_id):
    payment_request = get_object_or_404(PaymentRequest, id=request_id)

    sender = payment_request.sender.user
    recipient = payment_request.recipient.user
    amount = payment_request.amount

    if sender.userprofile.balance >= amount:
        recipient_currency, converted_amount = make_transaction(amount, recipient, sender)

        payment_request.is_accepted = True
        payment_request.save()

        messages.success(request,
                         f'Payment was successful. \n{converted_amount} {recipient_currency} was sent to {recipient.username}.')
    else:
        messages.error(request, 'Payment request could not be accepted.')

    return redirect(reverse('notifications'))


@transaction.atomic
def decline_payment_request(request, request_id):
    payment_request = get_object_or_404(PaymentRequest, id=request_id)

    payment_request.is_accepted = False
    payment_request.save()

    messages.success(request, 'Payment request declined.')

    return redirect(reverse('notifications'))


@csrf_exempt
def convert_currency(request, currency1, currency2, amount_of_currency1):
    if request.method != 'GET':
        return HttpResponseNotAllowed(request.method)

    currency_rate = CurrencyRate()
    try:
        rate = currency_rate.get_rate(currency1, currency2)
        converted_amount = rate * amount_of_currency1
        timestamp = get_timestamp()

        return JsonResponse({
            'converted_amount': converted_amount,
            'timestamp': timestamp
        })
    except KeyError:
        return HttpResponseBadRequest('One or both of the provided currencies are not supported.')
