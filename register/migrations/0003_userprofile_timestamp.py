# Generated by Django 4.2.11 on 2024-04-18 20:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        (
            "register",
            "0002_alter_userprofile_balance_alter_userprofile_currency_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="timestamp",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]