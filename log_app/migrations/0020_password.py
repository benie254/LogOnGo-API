# Generated by Django 4.1 on 2022-10-22 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0019_alter_myuser_employee_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Password',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=120, null=True)),
                ('email', models.EmailField(blank=True, max_length=120, null=True)),
            ],
        ),
    ]