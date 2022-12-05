from django import forms

from log_app.models import Announcement, Contact, Incident, Log, LogMpesa

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError

from django_registration.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
 
from .models import Fuel, FuelReceived, LogReport, MpesaReport, MyUser 
from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, identify_hasher
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _ 
from django.contrib.auth.forms import UsernameField,ReadOnlyPasswordHashField 


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta:
        model = MyUser
        fields = "__all__"
        field_classes = {"username": UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format("../password/")
        user_permissions = self.fields.get("user_permissions")
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related(
                "content_type"
            )

class MyRegForm(RegistrationForm):
    class Meta:
        model = MyUser
        fields = ('username','first_name','last_name','email','petrol_station')


class MyLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = MyUser
        fields = ('username',)