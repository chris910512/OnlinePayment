from django.db import models
from register.models import UserProfile


class Transaction(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.amount}"


class PaymentRequest(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='sent_payment_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='received_payment_requests', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.amount} Request"
