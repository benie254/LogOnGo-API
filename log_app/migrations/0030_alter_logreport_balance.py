# Generated by Django 4.1 on 2022-10-25 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0029_alter_logreport_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logreport',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True),
        ),
    ]
