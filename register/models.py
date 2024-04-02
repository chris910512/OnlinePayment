from django.contrib.auth.models import User
from django.db import models, transaction


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    currency = models.CharField(max_length=3)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000)

    def make_payment(self, recipient, amount):
        if self.balance >= amount:
            with transaction.atomic():
                self.balance -= amount
                self.save()
                recipient.balance += amount
                recipient.save()
                Transaction.objects.create(sender=self, recipient=recipient, amount=amount)
                return True
        return False

    def __str__(self):
        return self.user.username


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
