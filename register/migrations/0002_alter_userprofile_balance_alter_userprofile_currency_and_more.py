# Generated by Django 4.2.11 on 2024-04-01 00:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("register", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="balance",
            field=models.DecimalField(decimal_places=2, default=1000, max_digits=10),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="currency",
            field=models.CharField(max_length=3),
        ),
        migrations.DeleteModel(
            name="Currency",
        ),
    ]