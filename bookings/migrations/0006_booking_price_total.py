# Generated by Django 4.2.12 on 2024-12-08 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_delete_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='price_total',
            field=models.DecimalField(decimal_places=2, default=200000, max_digits=10),
            preserve_default=False,
        ),
    ]
