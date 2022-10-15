# Generated by Django 4.1 on 2022-10-14 02:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0006_alter_logcreditcard_card_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logcreditcard',
            name='card_number',
            field=models.BigIntegerField(validators=[django.core.validators.MinValueValidator(1000000000000000), django.core.validators.MaxValueValidator(9999999999999999)]),
        ),
    ]
