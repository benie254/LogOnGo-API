# Generated by Django 4.1 on 2022-09-21 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0009_logmpesa_amount_logmpesa_amount_transferred_to_bank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logmpesa',
            name='amount_transferred_to_bank',
            field=models.BigIntegerField(default=0),
        ),
    ]