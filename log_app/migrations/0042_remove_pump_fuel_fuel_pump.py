# Generated by Django 4.1 on 2022-11-03 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0041_alter_summary_fuel_alter_summary_pump'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pump',
            name='fuel',
        ),
        migrations.AddField(
            model_name='fuel',
            name='pump',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='log_app.pump'),
        ),
    ]
