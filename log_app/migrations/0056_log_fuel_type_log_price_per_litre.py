# Generated by Django 4.1 on 2022-11-23 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0055_remove_summary_log_log_amount_earned_today_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='fuel_type',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='log',
            name='price_per_litre',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
