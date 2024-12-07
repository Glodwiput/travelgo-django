# Generated by Django 4.2.12 on 2024-12-07 03:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bookings', '0003_delete_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_method', models.CharField(max_length=50)),
                ('payment_date', models.DateField()),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bookings.booking')),
            ],
        ),
    ]
