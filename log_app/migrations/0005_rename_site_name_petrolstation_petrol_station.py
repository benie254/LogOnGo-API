# Generated by Django 4.1 on 2022-09-12 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0004_profile_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='petrolstation',
            old_name='site_name',
            new_name='petrol_station',
        ),
    ]