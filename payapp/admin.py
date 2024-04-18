from django.contrib import admin

from payapp.models import Notification, PaymentRequest, Transaction

# Register your models here.

admin.site.register(Notification)
admin.site.register(Transaction)
admin.site.register(PaymentRequest)
