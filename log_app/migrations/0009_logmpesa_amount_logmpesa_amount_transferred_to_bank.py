# Generated by Django 4.1 on 2022-09-21 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0008_logmpesa_customer_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='logmpesa',
            name='amount',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='logmpesa',
            name='amount_transferred_to_bank',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
