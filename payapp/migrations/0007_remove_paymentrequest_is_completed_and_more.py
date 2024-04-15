# Generated by Django 4.2.11 on 2024-04-15 03:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payapp", "0006_notification_is_request_transaction"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="paymentrequest",
            name="is_completed",
        ),
        migrations.AddField(
            model_name="paymentrequest",
            name="is_accepted",
            field=models.BooleanField(default=False),
        ),
    ]
