# Generated by Django 4.1 on 2022-10-24 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0026_alter_deleterequest_litres_sold_today'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deleterequest',
            name='litres_sold_today',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=18, null=True),
        ),
    ]
