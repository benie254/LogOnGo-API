from rest_framework import serializers
from log_app.models import DeleteRequest, Fuel, FuelReceived, LogCreditCard, LogReport, MpesaReport, MyUser, Announcement, Contact, Incident, Log, LogMpesa, Pump, Site
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


class PumpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pump 
        fields = ('id','pump_name','date','initial_litres_in_tank','balance','updated_balance','balance_yesterday','total_litres_sold_today','amount_earned_today')

class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuel 
        fields = ('id','fuel_type','price_per_litre','pumps','initial_litres_in_tank','total_litres_sold_today','balance','updated_balance','balance_yesterday')

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log 
        fields = ('id','fuel','fuel_name','price_per_litre','pump','pump_name','date','formatted_date','eod_reading_lts','eod_reading_yesterday','total_litres_sold','amount_earned_today','first_logged','last_edited','edited_by','user_id','logged_by',)

class LogMpesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogMpesa 
        fields = ('id','fuel','fuel_name','date','transaction_number','user','logged_by','customer_name','customer_phone_number','amount','amount_transferred_to_bank','daily_total','cumulative_amount','first_logged','last_edited','edited_by')

class LogCreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogCreditCard
        fields = ('id','fuel','fuel_name','date','card_name','card_number','amount','daily_total','cumulative_amount','site_name','user','logged_by','first_logged','last_edited','edited_by')

class FuelReceivedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelReceived 
        fields = ('id','litres_received','received_from','date_received','fuel','fuel_name','total_fuel_received_today')

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident  
        fields = ('id','nature','description','reporter','your_name','your_email','incident_date','date_and_time_reported',)

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact  
        fields = ('id','subject','message','your_email','your_name',)

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement  
        fields = ('id','user_id','date','subject','announcement','announced_by',)

class LogReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogReport 
        fields = ('id','user','date','eod_reading_lts','eod_reading_yesterday','litres_sold_today','amount_earned_today','balance','first_logged','last_edited','admin_name','admin_email','logged_by',)

    # def create(self, validated_data):
    #     user = LogReport.objects.create_report(**validated_data)
    #     return user

class MpesaReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaReport 
        fields = ('id','date','transaction_number','customer_name','customer_phone_number','amount','amount_transferred_to_bank','daily_total','cumulative_amount','admin_name','admin_email','logged_by',)


class CreditCardReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogCreditCard
        fields = ('id','date','card_name','card_number','amount','logged_by','admin_name','admin_email')    

class DeleteLogRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteRequest
        fields = ('id','log_id','date','date_requested','eod_reading_lts','eod_reading_yesterday','litres_sold_today','amount_earned_today','balance','logged_by')

class DeleteMpesaRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteRequest
        fields = ('id','log_id','date','date_requested','transaction_number','amount','amount_transferred_to_bank','customer_name','customer_phone_number','logged_by')

class DeleteCreditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteRequest
        fields = ('id','log_id','date','date_requested','card_name','card_number','amount','logged_by','admin_name','admin_email','requested_by')


