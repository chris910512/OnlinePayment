from django.contrib import admin

from payapp.models import Notification, PaymentRequest

# Register your models here.

admin.site.register(Notification)
admin.site.register(PaymentRequest)
