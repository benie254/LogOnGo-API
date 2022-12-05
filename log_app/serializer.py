from rest_framework import serializers
from log_app.models import CreditCardReport, DeleteRequest, Fuel, FuelReceived, LogCreditCard, LogReport, MpesaReport, MyUser, Announcement, Contact, Incident, Log, LogMpesa, Site 
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


class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuel 
        fields = ('id','fuel_type','pp_litre','tank_init','pumps')

class FuelSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Log 
        fields = ('id','fuel','cumulative_litres_td','cumulative_amount_td','cumulative_bal_td')

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log 
        fields = ('id','fuel','fuel_type','pp_litre','tank_init','date','long_date','eod_reading','eod_yesterday','litres_sold','amount_td','bal','updated_bal','bal_yesterday','first_logged','last_edited','edited_by','user','logged_by','cumulative_litres_td','cumulative_amount_td','cumulative_bal_td')

class PumpSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Log 
        fields = ('id','date','fuel','litres_sold','amount_td','bal','updated_bal')

class LogMpesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogMpesa 
        fields = ('id','fuel','fuel_type','pp_litre','date','long_date','transaction_no','user','logged_by','customer','customer_no','amount','to_bank','total_td','cumulative_amount','first_logged','last_edited','edited_by')

class LogCreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogCreditCard
        fields = ('id','fuel','date','long_date','fuel_type','pp_litre','card_name','card_no','amount','total_td','cumulative_amount','user','logged_by','first_logged','last_edited','edited_by')

class FuelReceivedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelReceived 
        fields = ('id','litres','in_from','date','fuel','total_td')

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident  
        fields = ('id','nature','description','name','email','date','reported',)

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact  
        fields = ('id','subject','date','message','email','name',)

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement  
        fields = ('id','user','date','subject','announcement','announced_by',)

class LogReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogReport 
        fields = ('id','date','eod_reading','eod_yesterday','litres_sold','amount_td','bal','first_logged','last_edited','name','email','logged_by',)

    # def create(self, validated_data):
    #     user = LogReport.objects.create_report(**validated_data)
    #     return user

class MpesaReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaReport 
        fields = ('id','date','transaction_no','customer','customer_no','amount','to_bank','total_td','cumulative_amount','name','email','logged_by',)


class CreditCardReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCardReport
        fields = ('id','date','card_name','card_no','amount','total_td','cumulative_amount','logged_by','name','email')    

class DeleteLogRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteRequest
        fields = ('__all__')

class DeleteMpesaRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteRequest
        fields = ('__all__')

class DeleteCreditRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeleteRequest
        fields = ('__all__')


