# Generated by Django 4.1 on 2022-10-08 03:31

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0012_log_price_per_litre'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogCreditCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.BigIntegerField(default=0)),
                ('card_name', models.CharField(default='', max_length=120)),
                ('card_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(9999999999999999), django.core.validators.MaxValueValidator(9999999999999999)])),
                ('date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
    ]
