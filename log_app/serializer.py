from rest_framework import serializers
from log_app.models import Fuel, FuelReceived, LogReport, MpesaReport, MyUser, Announcement, Contact, Incident, Log, LogMpesa


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id','email','first_name','last_name','petrol_station')
        extra_kwargs = {
            'password':{'write_only':True}
        }     

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

                     