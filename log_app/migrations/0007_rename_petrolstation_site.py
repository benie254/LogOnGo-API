# Generated by Django 4.1 on 2022-09-12 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0006_alter_petrolstation_petrol_station'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PetrolStation',
            new_name='Site',
        ),
    ]