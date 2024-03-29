from django.contrib import admin

from payapp.models import Transaction, PaymentRequest

# Register your models here.

admin.site.register(Transaction)
admin.site.register(PaymentRequest)
