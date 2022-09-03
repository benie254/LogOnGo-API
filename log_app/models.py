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

# Create your models here.
class MyAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
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

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

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
        },
    )
    first_name = models.CharField(_("first name"), max_length=150,blank=True)
    last_name = models.CharField(_("last name"), max_length=150,blank=True)
    CHOICES = (('Station-Kisii','Station-Kisii'),('Station-Nairobi','Station-Nairobi'))
    petrol_station = models.CharField(_("petrol station"), max_length=150,choices=CHOICES,blank=True)
    email = models.EmailField(_("email address"), blank=True)
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
    REQUIRED_FIELDS = ['email','first_name','last_name',"petrol_station"]


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

# created upon successful registration
class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150)
    signup_confirmation = models.BooleanField(default=False) 

@receiver(post_save, sender=MyUser)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class PetrolStation(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=100,null=True)
    signup_confirmation = models.BooleanField(default=False) 

@receiver(post_save, sender=MyUser)
def update_petrol_station_signal(sender, instance, created, **kwargs):
    if created:
        PetrolStation.objects.create(user=instance)

class Fuel(models.Model):
    CHOICES = (('Petrol','Petrol'),('Diesel','Diesel'),('Gas','Gas'))
    fuel_type = models.CharField(max_length=60,choices=CHOICES,null=True,blank=True)
    price_per_litre = models.IntegerField()
    pumps = models.PositiveIntegerField()
    initial_litres_in_tank = models.IntegerField()

    def __int__(self):
        return self.price_per_litre

class Log(models.Model):
    date = models.DateField(default=timezone.now,null=True,blank=True)
    fuel = models.ForeignKey(Fuel,on_delete=models.CASCADE,null=True,blank=True)
    eod_reading_lts = models.IntegerField()
    eod_reading_yesterday = models.IntegerField(null=True,blank=True)
    balance = models.PositiveIntegerField(null=True,blank=True)
    balance_yesterday = models.PositiveIntegerField(null=True,blank=True)
    first_logged = models.DateTimeField(auto_now_add=True,null=True)
    last_edited =models.DateTimeField(auto_now=True,null=True,blank=True)
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)
    logged_by = models.CharField(max_length=120,null=True,blank=True)
    site_name = models.ForeignKey(PetrolStation,on_delete=models.CASCADE,null=True,blank=True)

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
            return redirect('home') 

        past_logs = cls.objects.filter(date=log_date)
        return past_logs

class LogMpesa(models.Model):
    date = models.DateField(default=timezone.now)
    transaction_number = models.PositiveIntegerField()
    customer_name = models.CharField(max_length=120)
    customer_phone_number = models.PositiveBigIntegerField()
    amount = models.PositiveBigIntegerField()
    amount_transferred_to_bank = models.BigIntegerField(null=True,blank=True)
    daily_total = models.BigIntegerField(null=True,blank=True)
    cumulative_amount = models.IntegerField(null=True,blank=True)
    first_logged = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    last_edited =models.DateTimeField(auto_now=True,null=True,blank=True)
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)
    logged_by = models.CharField(max_length=120,blank=True,null=True)
    site_name = models.ForeignKey(PetrolStation,on_delete=models.CASCADE,null=True,blank=True)

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
            return redirect('home') 

        past_logs = cls.objects.filter(date=log_date)
        return past_logs

class FuelReceived(models.Model):
    litres_received = models.PositiveIntegerField()
    received_from = models.CharField(max_length=100)
    date_received = models.DateField(default=timezone.now)
    fuel = models.ForeignKey(Fuel,on_delete=models.CASCADE,null=True,blank=True)

    def __int__(self):
        return self.litres_received 


class Incident(models.Model):
    CHOICES = (('Equipment Failure','Equipment Failure'),('Physical Injury','Physical Injury'),('EMERGENCY','EMERGENCY'))
    nature = models.CharField(max_length=100,choices=CHOICES)
    description = models.TextField(max_length=5000)
    reporter = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)
    your_name = models.CharField(max_length=120,null=True,blank=True)
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
    your_name = models.CharField(max_length=120,null=True,blank=True) 
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.announcement

class LogReport(models.Model):
    date = models.DateField(null=True,blank=True)
    eod_reading_lts = models.IntegerField(null=True,blank=True)
    eod_reading_yesterday = models.IntegerField(null=True,blank=True)
    litres_sold_today = models.IntegerField(null=True,blank=True)
    amount_earned_today = models.PositiveBigIntegerField(null=True,blank=True)
    balance = models.PositiveIntegerField(null=True,blank=True)
    first_logged = models.DateTimeField(null=True,blank=True)
    last_edited =models.DateTimeField(null=True,blank=True)
    logged_by = models.CharField(max_length=120,null=True,blank=True)
    admin_name = models.CharField(max_length=120,null=True,blank=True)
    admin_email = models.EmailField(max_length=120,null=True,blank=True)

    def __int__(self):
        return self.eod_reading_lts

class MpesaReport(models.Model):
    date = models.DateField(blank=True,null=True)
    transaction_number = models.PositiveIntegerField(blank=True,null=True)
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