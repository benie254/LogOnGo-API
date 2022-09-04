from rest_framework import serializers, exceptions
from log_app.models import Fuel, FuelReceived, LogReport, MpesaReport, MyUser, Announcement, Contact, Incident, Log, LogMpesa, PetrolStation
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.password_validation import validate_password

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
# from .tokens import account_activation_token
from django.template.loader import render_to_string 
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from log_app.utils import validate_email as email_is_valid


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id','email','first_name','last_name','petrol_station')
        extra_kwargs = {
            'password':{'write_only':True}
        }   
class UserRegSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    # class Meta:
    #     model = MyUser
    #     fields = ('username','email','first_name','last_name','petrol_station','password')
    
    # def validate_email(self,value: str) -> str:
    #     valid, error_text = email_is_valid(value)
    #     if not valid:
    #         raise serializers.ValidationError(error_text)
    #     try:
    #         email_name, domain_part = value.strip().rsplit('@', 1)
    #     except ValueError:
    #         pass
    #     else:
    #         value = '@'.join([email_name, domain_part.lower()])
    #     return value

    def create(self, data):
        user = MyUser.objects.create_user(
            email=data.get('email'),
            username=data.get('username'),
            password=data.get('password'),
        )
        user.first_name = data.get('first_name','')
        user.last_name = data.get('last_name','')
        user.petrol_station = data.get('petrol_station','')
        user.save()
        return user

    # password = serializers.CharField(
    #     max_length=128,
    #     min_length=8,
    #     write_only=True
    # )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    # token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = MyUser
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email','username', 'first_name', 'last_name', 'petrol_station']

    

class LoginSerializer(serializers.ModelSerializer[MyUser]):
    email = serializers.EmailField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):  # type: ignore
        """Get user token."""
        user = MyUser.objects.get(email=obj.email)

        return {'refresh': user.tokens['refresh'], 'access': user.tokens['access']}

    class Meta:
        model = MyUser
        fields = ['email','username', 'password', 'tokens', 'is_staff']

    def validate(self, data):  # type: ignore
        """Validate and return user login."""
        password = data.get('password', None)
        email = data.get('email', None)
        username = data.get('username', None)

        if email is None:
            raise serializers.ValidationError('An email address is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=username, email=email, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this username and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user is not currently activated.')

        return user


class UserSerializer(serializers.ModelSerializer[MyUser]):
    """Handle serialization and deserialization of MyUser objects."""

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = MyUser
        fields = (
            'email',
            'username',
            'password',
            'tokens',
            'first_name',
            'last_name',
            'petrol_station',
            'is_staff',
        )
        read_only_fields = ('tokens', 'is_staff')

    def update(self, instance, validated_data):  # type: ignore
        """Perform an update on a MyUser."""

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class LogoutSerializer(serializers.Serializer[MyUser]):
    refresh = serializers.CharField()

    def validate(self, attrs):  # type: ignore
        """Validate token."""
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):  # type: ignore
        """Validate save backlisted token."""

        try:
            RefreshToken(self.token).blacklist()

        except TokenError as ex:
            raise exceptions.AuthenticationFailed(ex)