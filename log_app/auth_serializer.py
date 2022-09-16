from rest_framework import serializers
from log_app.models import MyUser, Site, Profile, Site

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from log_app.models import MyUser as User

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id', 'employee_id', 'username', 'email', 'first_name', 'last_name', 'petrol_station', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile 
        fields = ('first_name', 'last_name', 'username', 'petrol_station', 'employee_id')

class UserRegistrationSerializer(serializers.ModelSerializer):

    profile = MyUserSerializer(required=False)

    class Meta:
        model = User
        fields = ('email', 'password','profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    employee_id = serializers.IntegerField()
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        employee_id = data.get("employee_id", None)
        password = data.get("password", None)
        user = authenticate(email=email, employee_id=employee_id, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email':user.email,
            'id':user.id,
            'token': jwt_token
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile 
        fields = ('id','first_name','last_name','username','email')

class PetrolStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = ('id','user_id','petrol_station')