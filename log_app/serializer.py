from rest_framework import serializers
from log_app.models import Fuel, FuelReceived, LogReport, MpesaReport, MyUser, Announcement, Contact, Incident, Log, LogMpesa, PetrolStation
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
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

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id','email','first_name','last_name','petrol_station')
        extra_kwargs = {
            'password':{'write_only':True}
        }   
class UserRegSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=MyUser.objects.all())])  
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True,required=True)
    class Meta:
        model = MyUser
        fields = ('username','password','password2','email','first_name','last_name','petrol_station')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True},
            'petrol_station': {'required': True},
        }
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Please match the password fields."}
            )
        return attrs 
    def create(self, validate_data):
        user = MyUser.objects.create(
            username = validate_data['username'],
            email = validate_data['email'],
            first_name = validate_data['first_name'],
            last_name = validate_data['last_name'],
            petrol_station = validate_data['petrol_station']
        )
        user.set_password(validate_data['password'])
        user.save()
        user.refresh_from_db()
        user.profile.username = validate_data['username']
        user.profile.first_name = validate_data['first_name']
        user.profile.last_name = validate_data['last_name']
        user.profile.petrol_station = validate_data['petrol_station']
        user.profile.email = validate_data['email']
        user.save()
        user.refresh_from_db()
        user.petrol_station.site_name = validate_data['petrol_station']
        user.save()
        return user 

class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuel 
        fields = ('id','fuel_type','price_per_litre','pumps','initial_litres_in_tank',)

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log 
        fields = ('id','fuel','date','eod_reading_lts','eod_reading_yesterday','balance','balance_yesterday','first_logged','last_edited','user','logged_by',)

class LogMpesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogMpesa 
        fields = ('id','date','transaction_number','customer_name','customer_phone_number','amount','amount_transferred_to_bank','daily_total','cumulative_amount','first_logged','last_edited','user','logged_by',)

class FuelReceivedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelReceived 
        fields = ('id','litres_received','received_from','date_received','fuel',)

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident  
        fields = ('id','nature','description','reporter','your_name','incident_date','date_and_time_reported',)

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact  
        fields = ('id','subject','message','your_email','your_name',)

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement  
        fields = ('id','subject','announcement','user','your_name',)

class LogReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogReport 
        fields = ('id','date','eod_reading_lts','eod_reading_yesterday','litres_sold_today','amount_earned_today','balance','first_logged','last_edited','admin_name','admin_email','logged_by',)

class MpesaReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaReport 
        fields = ('id','date','transaction_number','customer_name','customer_phone_number','amount','amount_transferred_to_bank','daily_total','cumulative_amount','admin_name','admin_email','logged_by',)

                     