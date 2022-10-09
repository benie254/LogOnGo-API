from django.db import models
from django.http import Http404
from django.shortcuts import redirect
from django.utils import timezone 
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,BaseUserManager
import datetime as dt 
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.apps import apps
from django.contrib import auth
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
class MyAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        # if not username:
        #     raise ValueError("The given username must be set")

        # if username is None:
        #     raise TypeError('Users must have a username.')

        # if email is None:
        #     raise TypeError('Users must have an email address.')

        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if password is None:
            raise TypeError('Admins must have a password.')

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()

    # A few helper functions for common logic between User and AnonymousUser.
    def _user_get_permissions(user, obj, from_name):
        permissions = set()
        name = "get_%s_permissions" % from_name
        for backend in auth.get_backends():
            if hasattr(backend, name):
                permissions.update(getattr(backend, name)(user, obj))
        return permissions


    def _user_has_perm(user, perm, obj):
        """
        A backend can raise `PermissionDenied` to short-circuit permission checking.
        """
        for backend in auth.get_backends():
            if not hasattr(backend, "has_perm"):
                continue
            try:
                if backend.has_perm(user, perm, obj):
                    return True
            except PermissionDenied:
                return False
        return False


    def _user_has_module_perms(user, app_label):
        """
        A backend can raise `PermissionDenied` to short-circuit permission checking.
        """
        for backend in auth.get_backends():
            if not hasattr(backend, "has_module_perms"):
                continue
            try:
                if backend.has_module_perms(user, app_label):
                    return True
            except PermissionDenied:
                return False
        return False


class MyUser(AbstractBaseUser,PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    
    username = models.CharField(
        _("username"),
        max_length=60,
        unique=True,
        help_text=_(
            "Required. 60 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        }
    )
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    CHOICES = (('Station-Kisii','Station-Kisii'),('Station-Nairobi','Station-Nairobi'))
    petrol_station = models.CharField(_("petrol station"), max_length=150,choices=CHOICES)
    email = models.EmailField(_("email address"),unique=True)
    IDS = ((12345,12345),(67891,67891),(102030,102030),(405060,405060),(708090,708090),(112233,112233),(445566,445566),(778899,778899),(101010,101010),(202020,202020),(303030,303030),(404040,404040),(505050,505050))
    employee_id = models.PositiveIntegerField(choices=IDS,unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = MyAccountManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email','employee_id','first_name','last_name',"petrol_station"]


    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)

    @property
    def tokens(self) -> dict[str, str]:
        """Allow us to get a user's token by calling `user.token`."""
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}

# created upon successful registration
class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    petrol_station = models.CharField(max_length=150,blank=True)
    signup_confirmation = models.BooleanField(default=False) 

@receiver(post_save, sender=MyUser)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Site(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    petrol_station = models.CharField(max_length=100,null=True,blank=True)
    signup_confirmation = models.BooleanField(default=False) 

@receiver(post_save, sender=MyUser)
def update_site_signal(sender, instance, created, **kwargs):
    if created:
        Site.objects.create(user=instance)
    instance.site.save()

class Fuel(models.Model):
    CHOICES = (('Petrol','Petrol'),('Diesel','Diesel'),('Gas','Gas'))
    fuel_type = models.CharField(max_length=60,choices=CHOICES)
    price_per_litre = models.DecimalField(max_digits=5,decimal_places=2)
    pumps = models.PositiveIntegerField()
    initial_litres_in_tank = models.DecimalField(max_digits=8,decimal_places=2)
    date = models.DateField(default=timezone.now,null=True,blank=True)
    balance = models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True)
    updated_balance = models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True)
    balance_yesterday = models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True)
    total_litres_sold_today = models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True)
    amount_earned_today = models.PositiveBigIntegerField(null=True,blank=True)

    def __int__(self):
        return self.price_per_litre

class Pump(models.Model):
    PUMPS = (('Pump One','Pump One'),('Pump Two','Pump Two'),('Pump Three','Pump Three'),('Pump Four','Pump Four'))
    pump_name = models.CharField(max_length=60,choices=PUMPS,default='')
    initial_litres_in_tank = models.DecimalField(max_digits=8,decimal_places=2,default=0)
    date = models.DateField(default=timezone.now,null=True,blank=True)
    balance = models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True)
    updated_balance = models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True)
    balance_yesterday = models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True)
    total_litres_sold_today = models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True)
    amount_earned_today = models.PositiveBigIntegerField(null=True,blank=True)

    def __str__(self):
        return self.pump_name
    
class Log(models.Model):
    date = models.DateField(default=timezone.now)
    fuel = models.ForeignKey(Fuel,on_delete=models.CASCADE,null=True,blank=True)
    fuel_name = models.CharField(max_length=60,null=True,blank=True)
    price_per_litre = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    pump = models.ForeignKey(Pump,on_delete=models.CASCADE,null=True)
    pump_name = models.CharField(max_length=60,null=True,blank=True)
    eod_reading_lts = models.DecimalField(max_digits=19,decimal_places=2)
    eod_reading_yesterday = models.DecimalField(max_digits=19,decimal_places=2,null=True,blank=True)
    total_litres_sold = models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True,default=0)
    amount_earned_today = models.PositiveBigIntegerField(null=True,blank=True)
    first_logged = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    last_edited =models.DateTimeField(auto_now=True,null=True,blank=True)
    user_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)
    logged_by = models.CharField(max_length=120,null=True,blank=True)
    site_name = models.ForeignKey(Site,on_delete=models.CASCADE,null=True,blank=True)

    def __int__(self):
        return self.eod_reading_lts

    @classmethod 
    def search_by_date(cls,log_date):
        try:
        # convert data from the string url
            date = dt.datetime.strptime(log_date, '%Y-%m-%d').date()

        except ValueError:
        # raise 404 when value error is thrown
            raise Http404()
            assert False

        if date == dt.date.today():
            today = dt.date.today()
            today_logs = cls.objects.filter(date=today)
            return today_logs 

        past_logs = cls.objects.filter(date=log_date)
        return past_logs

class LogMpesa(models.Model):
    date = models.DateField(default=timezone.now)
    fuel = models.ForeignKey(Fuel,on_delete=models.CASCADE,null=True,blank=True)
    transaction_number = models.CharField(max_length=30,default=0)
    customer_name = models.CharField(max_length=120,default='')
    customer_phone_number = models.PositiveBigIntegerField(default=0)
    amount = models.PositiveBigIntegerField(default=0)
    amount_transferred_to_bank = models.BigIntegerField(default=0)
    daily_total = models.BigIntegerField(null=True,blank=True)
    cumulative_amount = models.IntegerField(null=True,blank=True)
    first_logged = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    last_edited =models.DateTimeField(auto_now=True,null=True,blank=True)
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)
    logged_by = models.CharField(max_length=120,blank=True,null=True)
    site_name = models.ForeignKey(Site,on_delete=models.CASCADE,null=True,blank=True)

    def __int__(self):
        return self.transaction_number 

    @classmethod
    def logs_today(cls):
        today = dt.date.today()
        day_mpesa_logs = cls.objects.filter(date__date=today)
        return day_mpesa_logs

    @classmethod 
    def search_by_date(cls,log_date):
        try:
        # convert data from the string url
            date = dt.datetime.strptime(log_date, '%Y-%m-%d').date()

        except ValueError:
        # raise 404 when value error is thrown
            raise Http404()
            assert False

        if date == dt.date.today():
            today = dt.date.today()
            today_logs = cls.objects.filter(date=today)
            return today_logs 

        past_logs = cls.objects.filter(date=log_date)
        return past_logs

class LogCreditCard(models.Model):
    fuel = models.ForeignKey(Fuel,on_delete=models.CASCADE,null=True,blank=True)
    amount = models.BigIntegerField(default=0)
    card_name = models.CharField(max_length=120,default='')
    card_number = models.IntegerField(validators=[MinValueValidator(9999999999999999),MaxValueValidator(9999999999999999)])
    date = models.DateField(default=timezone.now)
    logged_by = models.CharField(max_length=120,null=True,blank=True)
    daily_total = models.BigIntegerField(null=True,blank=True)
    cumulative_amount = models.IntegerField(null=True,blank=True)
    first_logged = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    last_edited =models.DateTimeField(auto_now=True,null=True,blank=True)
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)
    site_name = models.ForeignKey(Site,on_delete=models.CASCADE,null=True,blank=True)

    @classmethod 
    def search_by_date(cls,log_date):
        try:
        # convert data from the string url
            date = dt.datetime.strptime(log_date, '%Y-%m-%d').date()

        except ValueError:
        # raise 404 when value error is thrown
            raise Http404()
            assert False

        if date == dt.date.today():
            today = dt.date.today()
            today_logs = cls.objects.filter(date=today)
            return today_logs 

        past_logs = cls.objects.filter(date=log_date)
        return past_logs

class FuelReceived(models.Model):
    litres_received = models.PositiveIntegerField(default=0)
    received_from = models.CharField(max_length=100)
    date_received = models.DateField(default=timezone.now)
    fuel = models.ForeignKey(Fuel,on_delete=models.CASCADE,null=True,blank=True)
    # pump = models.ForeignKey(Pump,on_delete=models.CASCADE,null=True)
    fuel_name = models.CharField(max_length=60,null=True,blank=True)
    total_fuel_received_today = models.PositiveIntegerField(default=0,null=True,blank=True)

    def __int__(self):
        return self.litres_received 


class Incident(models.Model):
    CHOICES = (('equipment','equipment'),('injury','injury'),('emergency','emergency'))
    nature = models.CharField(max_length=100,choices=CHOICES)
    description = models.TextField(max_length=5000)
    reporter = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)
    your_name = models.CharField(max_length=120,null=True,blank=True)
    your_email = models.EmailField(max_length=250,null=True,blank=True)
    incident_date = models.DateField(default=timezone.now)
    date_and_time_reported = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.description

class Contact(models.Model):
    subject = models.CharField(max_length=60)
    message = models.TextField(max_length=5000)
    your_name = models.CharField(max_length=120,null=True,blank=True) 
    your_email = models.EmailField(max_length=150,null=True,blank=True)

    def __str__(self):
        return self.message 

class Announcement(models.Model):
    subject = models.CharField(max_length=60)
    announcement = models.TextField(max_length=5000) 
    date = models.DateField(default=timezone.now)
    announced_by = models.CharField(max_length=120,null=True,blank=True) 
    user_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.announcement

class LogReport(models.Model):
    user = models.ForeignKey(MyUser,null=True,on_delete=models.CASCADE)
    date = models.DateField(null=True,blank=True)
    eod_reading_lts = models.IntegerField(null=True,blank=True)
    eod_reading_yesterday = models.IntegerField(null=True,blank=True)
    litres_sold_today = models.IntegerField(null=True,blank=True)
    amount_earned_today = models.PositiveBigIntegerField(null=True,blank=True)
    balance = models.PositiveIntegerField(null=True,blank=True)
    first_logged = models.DateTimeField(null=True,blank=True)
    last_edited =models.DateTimeField(null=True,blank=True)
    logged_by = models.CharField(max_length=120,null=True,blank=True)
    admin_name = models.CharField(max_length=120,default='')
    admin_email = models.EmailField(max_length=120,default='')

    def __int__(self):
        return self.eod_reading_lts

class MpesaReport(models.Model):
    date = models.DateField(blank=True,null=True)
    transaction_number = models.CharField(max_length=100,blank=True,null=True)
    customer_name = models.CharField(max_length=120,blank=True,null=True)
    customer_phone_number = models.PositiveBigIntegerField(blank=True,null=True)
    amount = models.PositiveBigIntegerField(blank=True,null=True)
    amount_transferred_to_bank = models.BigIntegerField(null=True,blank=True)
    daily_total = models.BigIntegerField(null=True,blank=True)
    cumulative_amount = models.IntegerField(null=True,blank=True)
    logged_by = models.CharField(max_length=120,null=True,blank=True)
    admin_name = models.CharField(max_length=120,null=True,blank=True)
    admin_email = models.EmailField(max_length=120,null=True,blank=True)

    def __int__(self):
        return self.transaction_number

class CreditCardReport(models.Model):
    amount = models.BigIntegerField(null=True,blank=True)
    card_name = models.CharField(max_length=120,null=True,blank=True)
    card_number = models.IntegerField(null=True,blank=True)
    date = models.DateField(default=timezone.now,null=True,blank=True)
    logged_by = models.CharField(max_length=120,null=True,blank=True)
    admin_name = models.CharField(max_length=120,null=True,blank=True)
    admin_email = models.EmailField(max_length=120,null=True,blank=True)