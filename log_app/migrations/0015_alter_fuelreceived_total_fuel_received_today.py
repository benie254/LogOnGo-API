# Generated by Django 4.1 on 2022-09-22 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0014_logreport_user_alter_logreport_admin_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuelreceived',
            name='total_fuel_received_today',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
