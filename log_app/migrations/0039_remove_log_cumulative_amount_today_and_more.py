# Generated by Django 4.1 on 2022-11-02 03:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0038_remove_fuel_amount_earned_today_remove_fuel_balance_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='cumulative_amount_today',
        ),
        migrations.RemoveField(
            model_name='log',
            name='cumulative_balance_today',
        ),
        migrations.RemoveField(
            model_name='log',
            name='cumulative_litres_sold_today',
        ),
        migrations.AddField(
            model_name='pump',
            name='fuel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='log_app.fuel'),
        ),
        migrations.CreateModel(
            name='FuelSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('cumulative_litres_sold_today', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=18, null=True)),
                ('cumulative_amount_today', models.PositiveBigIntegerField(blank=True, null=True)),
                ('cumulative_balance_today', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('fuel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='log_app.fuel')),
                ('pump', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='log_app.pump')),
            ],
        ),
    ]
