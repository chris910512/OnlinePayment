from django.contrib.auth.models import User
from django.db import models

from register.models import UserProfile


class PaymentRequest(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_payment_requests', on_delete=models.CASCADE)
    recipient = models.ForeignKey(UserProfile, related_name='received_payment_requests', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} -> {self.recipient}: {self.amount} Request"


class Notification(models.Model):
    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.userprofile.first_name} {self.sender.userprofile.last_name} ' \
               f'sent {self.amount} to {self.recipient.userprofile.first_name} {self.recipient.userprofile.last_name}'
