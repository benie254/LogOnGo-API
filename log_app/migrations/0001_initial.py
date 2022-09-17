# Generated by Django 4.1 on 2022-09-17 04:55

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import log_app.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 60 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=60, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(max_length=150, verbose_name='last name')),
                ('petrol_station', models.CharField(choices=[('Station-Kisii', 'Station-Kisii'), ('Station-Nairobi', 'Station-Nairobi')], max_length=150, verbose_name='petrol station')),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('employee_id', models.PositiveIntegerField(choices=[(12345, 12345), (67891, 67891), (102030, 102030), (405060, 405060), (708090, 708090), (112233, 112233), (445566, 445566), (778899, 778899), (101010, 101010), (202020, 202020), (303030, 303030), (404040, 404040), (505050, 505050)], unique=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', log_app.models.MyAccountManager()),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=60)),
                ('message', models.TextField(max_length=5000)),
                ('your_name', models.CharField(blank=True, max_length=120, null=True)),
                ('your_email', models.EmailField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fuel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fuel_type', models.CharField(choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('Gas', 'Gas')], max_length=60)),
                ('price_per_litre', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pumps', models.PositiveIntegerField()),
                ('initial_litres_in_tank', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='LogReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('eod_reading_lts', models.IntegerField(blank=True, null=True)),
                ('eod_reading_yesterday', models.IntegerField(blank=True, null=True)),
                ('litres_sold_today', models.IntegerField(blank=True, null=True)),
                ('amount_earned_today', models.PositiveBigIntegerField(blank=True, null=True)),
                ('balance', models.PositiveIntegerField(blank=True, null=True)),
                ('first_logged', models.DateTimeField(blank=True, null=True)),
                ('last_edited', models.DateTimeField(blank=True, null=True)),
                ('logged_by', models.CharField(blank=True, max_length=120, null=True)),
                ('admin_name', models.CharField(blank=True, max_length=120, null=True)),
                ('admin_email', models.EmailField(blank=True, max_length=120, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MpesaReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('transaction_number', models.PositiveIntegerField(blank=True, null=True)),
                ('customer_name', models.CharField(blank=True, max_length=120, null=True)),
                ('customer_phone_number', models.PositiveBigIntegerField(blank=True, null=True)),
                ('amount', models.PositiveBigIntegerField(blank=True, null=True)),
                ('amount_transferred_to_bank', models.BigIntegerField(blank=True, null=True)),
                ('daily_total', models.BigIntegerField(blank=True, null=True)),
                ('cumulative_amount', models.IntegerField(blank=True, null=True)),
                ('logged_by', models.CharField(blank=True, max_length=120, null=True)),
                ('admin_name', models.CharField(blank=True, max_length=120, null=True)),
                ('admin_email', models.EmailField(blank=True, max_length=120, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('petrol_station', models.CharField(blank=True, max_length=100, null=True)),
                ('signup_confirmation', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('username', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(blank=True, max_length=150)),
                ('petrol_station', models.CharField(blank=True, max_length=150)),
                ('signup_confirmation', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LogMpesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('transaction_number', models.CharField(max_length=30)),
                ('customer_name', models.CharField(max_length=120)),
                ('customer_phone_number', models.PositiveBigIntegerField()),
                ('amount', models.PositiveBigIntegerField()),
                ('amount_transferred_to_bank', models.BigIntegerField(blank=True, null=True)),
                ('daily_total', models.BigIntegerField(blank=True, null=True)),
                ('cumulative_amount', models.IntegerField(blank=True, null=True)),
                ('first_logged', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_edited', models.DateTimeField(auto_now=True, null=True)),
                ('logged_by', models.CharField(blank=True, max_length=120, null=True)),
                ('site_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='log_app.site')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('eod_reading_lts', models.DecimalField(decimal_places=2, max_digits=19)),
                ('eod_reading_yesterday', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
                ('total_litres_sold', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('amount_earned_today', models.PositiveBigIntegerField(blank=True, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('updated_balance', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('balance_yesterday', models.DecimalField(blank=True, decimal_places=2, max_digits=18, null=True)),
                ('first_logged', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_edited', models.DateTimeField(auto_now=True, null=True)),
                ('logged_by', models.CharField(blank=True, max_length=120, null=True)),
                ('fuel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='log_app.fuel')),
                ('site_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='log_app.site')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nature', models.CharField(choices=[('Equipment Failure', 'Equipment Failure'), ('Physical Injury', 'Physical Injury'), ('EMERGENCY', 'EMERGENCY')], max_length=100)),
                ('description', models.TextField(max_length=5000)),
                ('your_name', models.CharField(blank=True, max_length=120, null=True)),
                ('incident_date', models.DateField(default=django.utils.timezone.now)),
                ('date_and_time_reported', models.DateTimeField(auto_now_add=True, null=True)),
                ('reporter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FuelReceived',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('litres_received', models.PositiveIntegerField()),
                ('received_from', models.CharField(max_length=100)),
                ('date_received', models.DateField(default=django.utils.timezone.now)),
                ('fuel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='log_app.fuel')),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=60)),
                ('announcement', models.TextField(max_length=5000)),
                ('your_name', models.CharField(blank=True, max_length=120, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
