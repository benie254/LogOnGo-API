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
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail 
import sendgrid
from sendgrid.helpers.mail import *
from decouple import config 
@receiver(reset_password_token_created)
def password_reset_token_created(instance, reset_password_token, *args, **kwargs):

    reset_msg = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)
    username = [reset_password_token.user.username]
    receiver = [reset_password_token.user.email]
    sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
    msg = "<p>We have received your request to reset your LogOnGo account password.</p><p>If you made this request, please click the following link to proceed with your password reset:</p><a>" + reset_msg + "</a>"
    message = Mail(
        from_email = Email("davinci.monalissa@gmail.com"),
        to_emails = receiver,
        subject = "Password Reset Request",
        html_content='<p>Hello, ' + str(username) + ', <br><br>' + msg
    )
    try:
        sendgrid_client = sendgrid.SendGridAPIClient(config('SENDGRID_API_KEY'))
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
        


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
            "unique": _("A user with this username already exists."),
        }
    )
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    CHOICES = (('Station-Kisii','Station-Kisii'),('Station-Nairobi','Station-Nairobi'))
    petrol_station = models.CharField(
        _("petrol station"), max_length=150,choices=CHOICES,
        error_messages={
            "invalid_choice": _("Value %r is an invalid choice."),
        }
        )
    email = models.EmailField(
        _("email address"),unique=True,
        error_messages={
            "unique": _("A user with this email already exists."),
        }
    )
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

    @property
    def tokens(self) -> dict[str, str]:
        """Allow us to get a user's token by calling `user.token`."""
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}

# created upon successful registration
class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE,blank=True,null=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=150, blank=True)
    petrol_station = models.CharField(max_length=150,blank=True)
    signup_confirmation = models.BooleanField(default=False) 
    is_staff = models.BooleanField(default=False) 
    is_superuser = models.BooleanField(default=False) 

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
    fuel_type = models.CharField(max_length=60,choices=CHOICES,default='')
    pp_litre = models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    pumps = models.PositiveIntegerField(default=0)
    tank_init = models.DecimalField(max_digits=8,decimal_places=2,default=0.00)
    
    def __int__(self):
        return self.pp_litre

class Log(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)
    fuel = models.ForeignKey(Fuel,on_delete=models.CASCADE,null=True,blank=True)
    fuel_type = models.CharField(max_length=60,null=True,blank=True)
    pp_litre = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    date = models.DateField(default=timezone.now)
    long_date = models.CharField(max_length=200,null=True,blank=True)
    eod_reading = models.DecimalField(max_digits=19,decimal_places=2,default=0.00)
    eod_yesterday = models.DecimalField(max_digits=19,decimal_places=2,default=0.00)
    litres_sold = models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True)
    amount_td = models.PositiveBigIntegerField(null=True,blank=True)
    bal = models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True)
    bal_yesterday = models.DecimalField(max_digits=18,decimal_places=2,default=0.00)
    updated_bal = models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True)
    cumulative_litres_td = models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True)
    cumulative_amount_td = models.PositiveBigIntegerField(null=True,blank=True)
    cumulative_bal_td = models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True)
    first_logged = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    logged_by = models.CharField(max_length=120,null=True,blank=True)
    last_edited =models.DateTimeField(auto_now=True,null=True,blank=True)
    edited_by = models.CharField(max_length=120,null=True,blank=True)

    def __int__(self):
        return self.eod_reading

class LogMpesa(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)
    fuel = models.ForeignKey(Fuel,on_delete=models.CASCADE,null=True,blank=True)
    fuel_type = models.CharField(max_length=60,null=True,blank=True)
    pp_litre = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    date = models.DateField(default=timezone.now)
    long_date = models.CharField(max_length=200,null=True,blank=True)
    transaction_no = models.CharField(max_length=30,default='')
    customer = models.CharField(max_length=120,default='')
    customer_no = models.PositiveBigIntegerField(default=0)
    amount = models.PositiveBigIntegerField(default=0)
    to_bank = models.BigIntegerField(default=0)
    total_td = models.BigIntegerField(null=True,blank=True)
    cumulative_amount = models.IntegerField(null=True,blank=True)
    first_logged = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    logged_by = models.CharField(max_length=120,blank=True,null=True)
    last_edited =models.DateTimeField(auto_now=True,null=True,blank=True)
    edited_by = models.CharField(max_length=120,null=True,blank=True)

    def __int__(self):
        return self.transaction_no

class LogCreditCard(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)
    fuel = models.ForeignKey(Fuel,on_delete=models.CASCADE,null=True,blank=True)
    fuel_type = models.CharField(max_length=60,null=True,blank=True)
    pp_litre = models.DecimalField(max_digits=5,decimal_places=2,null=True,blank=True)
    date = models.DateField(default=timezone.now)
    long_date = models.CharField(max_length=200,null=True,blank=True)
    card_name = models.CharField(max_length=120,default='')
    card_no = models.BigIntegerField(validators=[MinValueValidator(1000000000000000),MaxValueValidator(9999999999999999)],default=0)
    amount = models.BigIntegerField(default=0)
    total_td = models.BigIntegerField(null=True,blank=True)
    cumulative_amount = models.IntegerField(null=True,blank=True)
    logged_by = models.CharField(max_length=120,null=True,blank=True)
    first_logged = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    last_edited =models.DateTimeField(auto_now=True,null=True,blank=True)
    edited_by = models.CharField(max_length=120,null=True,blank=True)

    def __str__(self):
        return self.card_name

class FuelReceived(models.Model):
    fuel = models.ForeignKey(Fuel,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(default=timezone.now)
    litres = models.PositiveIntegerField(default=0)
    in_from = models.CharField(max_length=100,default=0)
    total_td = models.PositiveBigIntegerField(default=0)

    def __int__(self):
        return self.litres

class Incident(models.Model):
    date = models.DateField(default=timezone.now)
    CHOICES = (('equipment','equipment'),('injury','injury'),('emergency','emergency'))
    nature = models.CharField(max_length=100,choices=CHOICES,default='')
    description = models.TextField(max_length=5000,default='')
    name = models.CharField(max_length=120,default='')
    email = models.EmailField(max_length=250,null=True,blank=True)
    reported = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.description

class Contact(models.Model):
    date = models.DateField(default=timezone.now)
    subject = models.CharField(max_length=60,default='')
    message = models.TextField(max_length=5000,default='')
    name = models.CharField(max_length=120,default='') 
    email = models.EmailField(max_length=150,default='')

    def __str__(self):
        return self.message 

class Announcement(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(default=timezone.now)
    subject = models.CharField(max_length=60,default='')
    announcement = models.TextField(max_length=5000,default='') 
    announced_by = models.CharField(max_length=120,null=True,blank=True) 

    def __str__(self):
        return self.announcement

class LogReport(models.Model):
    date = models.DateField(null=True,blank=True)
    eod_reading = models.DecimalField(max_digits=19,decimal_places=2,null=True,blank=True)
    eod_yesterday = models.DecimalField(max_digits=19,decimal_places=2,null=True,blank=True)
    litres_sold = models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True)
    amount_td = models.PositiveBigIntegerField(null=True,blank=True)
    bal = models.DecimalField(max_digits=18,decimal_places=2,null=True,blank=True)
    first_logged = models.DateTimeField(null=True,blank=True)
    logged_by = models.CharField(max_length=120,null=True,blank=True)
    last_edited =models.DateTimeField(null=True,blank=True)
    name = models.CharField(max_length=120,default='')
    email = models.EmailField(max_length=120,default='')

    def __int__(self):
        return self.eod_reading

class MpesaReport(models.Model):
    date = models.DateField(blank=True,null=True)
    transaction_no = models.CharField(max_length=100,blank=True,null=True)
    customer = models.CharField(max_length=120,blank=True,null=True)
    customer_no = models.PositiveBigIntegerField(blank=True,null=True)
    amount = models.PositiveBigIntegerField(blank=True,null=True)
    to_bank = models.BigIntegerField(null=True,blank=True)
    total_td = models.BigIntegerField(null=True,blank=True)
    cumulative_amount = models.IntegerField(null=True,blank=True)
    logged_by = models.CharField(max_length=120,null=True,blank=True)
    name = models.CharField(max_length=120,null=True,blank=True)
    email = models.EmailField(max_length=120,null=True,blank=True)

    def __int__(self):
        return self.transaction_no

class CreditCardReport(models.Model):
    date = models.DateField(default=timezone.now,null=True,blank=True)
    card_name = models.CharField(max_length=120,null=True,blank=True)
    card_no = models.BigIntegerField(null=True,blank=True,validators=[MinValueValidator(1000000000000000),MaxValueValidator(9999999999999999)])
    amount = models.BigIntegerField(null=True,blank=True)
    total_td = models.BigIntegerField(null=True,blank=True)
    cumulative_amount = models.IntegerField(null=True,blank=True)
    logged_by = models.CharField(max_length=120,null=True,blank=True)
    name = models.CharField(max_length=120,null=True,blank=True)
    email = models.EmailField(max_length=120,null=True,blank=True)

    def __int__(self):
        return self.card_no

class Password(models.Model):
    username = models.CharField(max_length=120,null=True,blank=True)
    email = models.EmailField(max_length=120,null=True,blank=True)

class DeleteRequest(models.Model):
    log_id = models.IntegerField(null=True,blank=True)
    date = models.CharField(max_length=120,blank=True,null=True)
    date_requested = models.CharField(max_length=120,default=timezone.now)
    logged_by = models.CharField(max_length=120,null=True,blank=True)
    user = models.CharField(max_length=120,null=True,blank=True)
    admin = models.CharField(max_length=120,null=True,blank=True)
    admin_email = models.EmailField(max_length=120,null=True,blank=True)

    def __int__(self):
        return self.date
    