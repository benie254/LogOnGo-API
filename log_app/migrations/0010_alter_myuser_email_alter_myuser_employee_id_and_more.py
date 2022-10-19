# Generated by Django 4.1 on 2022-10-19 10:58

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0009_log_edited_by_logcreditcard_edited_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(error_messages={'unique': 'A user with this email already exists.'}, max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='employee_id',
            field=models.PositiveIntegerField(choices=[(12345, 12345), (67891, 67891), (102030, 102030), (405060, 405060), (708090, 708090), (112233, 112233), (445566, 445566), (778899, 778899), (101010, 101010), (202020, 202020), (303030, 303030), (404040, 404040), (505050, 505050)], error_messages={'unique': 'A user with this ID already exists.'}, unique=True),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with this username already exists.'}, help_text='Required. 60 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=60, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
