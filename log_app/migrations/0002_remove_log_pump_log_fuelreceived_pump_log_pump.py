# Generated by Django 4.1 on 2022-09-24 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='pump_log',
        ),
        migrations.AddField(
            model_name='fuelreceived',
            name='pump',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='log_app.pump'),
        ),
        migrations.AddField(
            model_name='log',
            name='pump',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='log_app.pump'),
        ),
    ]
