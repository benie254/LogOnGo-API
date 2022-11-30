# Generated by Django 4.1 on 2022-11-23 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0056_log_fuel_type_log_price_per_litre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deleterequest',
            name='admin_email',
            field=models.EmailField(blank=True, default='', max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='deleterequest',
            name='admin_name',
            field=models.CharField(blank=True, default='', max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='deleterequest',
            name='amount',
            field=models.PositiveBigIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='deleterequest',
            name='amount_earned_today',
            field=models.PositiveBigIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='deleterequest',
            name='amount_transferred_to_bank',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='deleterequest',
            name='balance',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='deleterequest',
            name='card_name',
            field=models.CharField(blank=True, default='', max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='deleterequest',
            name='card_number',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='deleterequest',
            name='customer_name',
            field=models.CharField(blank=True, default='', max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='deleterequest',
            name='customer_phone_number',
            field=models.PositiveBigIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='deleterequest',
            name='date',
            field=models.CharField(blank=True, default='', max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='deleterequest',
            name='eod_reading_lts',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=19, null=True),
        ),
        migrations.AlterField(
            model_name='deleterequest',
            name='eod_reading_yesterday',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=19, null=True),
        ),
        migrations.AlterField(
            model_name='deleterequest',
            name='log_id',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='deleterequest',
            name='logged_by',
            field=models.CharField(blank=True, default='', max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='deleterequest',
            name='requested_by',
            field=models.CharField(blank=True, default='', max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='deleterequest',
            name='transaction_number',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
