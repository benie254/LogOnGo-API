from rest_framework import serializers
from log_app.models import Fuel, FuelReceived, LogReport, MpesaReport, MyUser, Announcement, Contact, Incident, Log, LogMpesa


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id','username','email','first_name','last_name','petrol_station')

class FuelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fuel 
        fields = ('id','fuel_type','price_per_litre','pumps','initial_litres_in_tank',)

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log 
        fields = ('id','date','eod_reading_lts','eod_reading_yesterday','balance','balance_yesterday','first_logged','last_edited','user','logged_by',)

class LogMpesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogMpesa 
        fields = ('date','transaction_number','customer_naame','customer_phone_number','amount','amount_transferred_to_bank','daily_total','cumulative_amount','first_logged','last_edited','user','logged_by',)

class FuelReceivedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelReceived 
        fields = ('litres_received','received_from','date_received','fuel',)

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident  
        fields = ('nature','description','reporter','your_name','incident_date','date_and_time_reported',)

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact  
        fields = ('subject','message','your_email','your_name',)

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement  
        fields = ('subject','announcement','user','your_name',)

class LogReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogReport 
        fields = ('date','eod_reading_lts','eod_reading_yesterday','litres_sold_today','amount_earned_today','balance','first_logged','last_edited','admin_name','admin_email','logged_by',)

class MpesaReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaReport 
        fields = ('date','transaction_number','customer_name','customer_phone_number','amount','amount_transferred_to_bank','daily_total','cumulative_amount','admin_name','admin_email','logged_by',)

                     