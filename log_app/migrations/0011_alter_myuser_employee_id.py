# Generated by Django 4.1 on 2022-10-19 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('log_app', '0010_alter_myuser_email_alter_myuser_employee_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='employee_id',
            field=models.PositiveIntegerField(choices=[(12345, 12345), (67891, 67891), (102030, 102030), (405060, 405060), (708090, 708090), (112233, 112233), (445566, 445566), (778899, 778899), (101010, 101010), (202020, 202020), (303030, 303030), (404040, 404040), (505050, 505050)], error_messages={'choices': 'No user with this ID was found.', 'unique': 'A user with this ID already exists.'}, unique=True),
        ),
    ]
