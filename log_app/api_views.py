import sendgrid
from sendgrid.helpers.mail import * 
import os 
from decouple import config 
from django.shortcuts import get_object_or_404, render,redirect 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from log_app.serializer import ContactSerializer, FuelReceivedSerializer, FuelSerializer, IncidentSerializer, LogMpesaSerializer, LogReportSerializer, LogSerializer, AnnouncementSerializer,LogReport, MpesaReportSerializer, PumpSerializer


from django.http import HttpResponse,Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from log_app.models import Fuel, FuelReceived, LogReport, MpesaReport, MyUser, Pump, Incident
import datetime as dt 
from django.db.models import Sum
from django.contrib import messages

from django.db.models import Max, Min,F, ExpressionWrapper, DecimalField, PositiveIntegerField

from log_app.models import Announcement, Contact, Incident, Log, LogMpesa
from rest_framework.permissions import AllowAny,AllowAny
# Create your views here.
class Announcements(APIView):
    permission_classes=(AllowAny,)
    def get_announcements(self):
        try:
            return Announcement.objects.all().order_by('-date')[:3]
        except Announcement.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        announcement = Announcement.objects.all().order_by('-date')[:3]
        serializers = AnnouncementSerializer(announcement,many=True)
        return Response(serializers.data)


class AllAnnouncements(APIView):
    permission_classes=(AllowAny,)
    def get_announcements(self):
        try:
            return Announcement.objects.all().order_by('-date')
        except Announcement.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        announcement = Announcement.objects.all().order_by('-date')
        serializers = AnnouncementSerializer(announcement,many=True)
        return Response(serializers.data)

class RegisteredFuels(APIView):
    permission_classes=(AllowAny,)
    def get_registered_fuels(self):
        try:
            return Fuel.objects.all()
        except Fuel.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        fuuel_info = Fuel.objects.all()
        serializers = FuelSerializer(fuuel_info,many=True)
        return Response(serializers.data)

class GasInfo(APIView):
    permission_classes=(AllowAny,)
    def get_gas_info(self):
        try:
            return Fuel.objects.all().filter(fuel_type='Gas').last()
        except Fuel.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        gas_info = Fuel.objects.all().filter(fuel_type='Gas').last()
        serializers = FuelSerializer(gas_info,many=False)
        return Response(serializers.data)

    def put(self, request, format=None):
        gas_info = Fuel.objects.all().filter(fuel_type='Gas').last()
        serializers = FuelSerializer(gas_info,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class DieselInfo(APIView):
    permission_classes=(AllowAny,)
    def get_diesel_info(self):
        try:
            return Fuel.objects.all().filter(fuel_type='Diesel').last()
        except Fuel.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        diesel_info = Fuel.objects.all().filter(fuel_type='Diesel').last()
        serializers = FuelSerializer(diesel_info,many=False)
        return Response(serializers.data)

    def put(self, request, format=None):
        gas_info = Fuel.objects.all().filter(fuel_type='Diesel').last()
        serializers = FuelSerializer(gas_info,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class PetrolInfo(APIView):
    permission_classes=(AllowAny,)
    def get_petrol_info(self):
        try:
            return Fuel.objects.all().filter(fuel_type='Petrol').last()
        except Fuel.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        petrol_info = Fuel.objects.all().filter(fuel_type='Petrol').last()
        serializers = FuelSerializer(petrol_info,many=False)
        return Response(serializers.data)

    def put(self, request, format=None):
        gas_info = Fuel.objects.all().filter(fuel_type='Petrol').last()
        serializers = FuelSerializer(gas_info,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class PumpOneInfo(APIView):
    permission_classes=(AllowAny,)
    def get_pump_info(self):
        try:
            return Pump.objects.all().filter(pump_name='Petrol').last()
        except Pump.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        pump_info = Pump.objects.all().filter(pump_name='Pump One').last()
        serializers = PumpSerializer(pump_info,many=False)
        return Response(serializers.data)

    def put(self, request, format=None):
        pump_info = Pump.objects.all().filter(pump_name='Pump One').last()
        serializers = PumpSerializer(pump_info,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class PumpTwoInfo(APIView):
    permission_classes=(AllowAny,)
    def get_pump_info(self):
        try:
            return Pump.objects.all().filter(pump_name='Pump Two').last()
        except Pump.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        pump_info = Pump.objects.all().filter(pump_name='Pump Two').last()
        serializers = PumpSerializer(pump_info,many=False)
        return Response(serializers.data)

    def put(self, request, format=None):
        pump_info = Pump.objects.all().filter(pump_name='Pump Two').last()
        serializers = PumpSerializer(pump_info,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class PumpThreeInfo(APIView):
    permission_classes=(AllowAny,)
    def get_pump_info(self):
        try:
            return Pump.objects.all().filter(pump_name='Pump Three').last()
        except Pump.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        pump_info = Pump.objects.all().filter(pump_name='Pump Three').last()
        serializers = PumpSerializer(pump_info,many=False)
        return Response(serializers.data)

    def put(self, request, format=None):
        pump_info = Pump.objects.all().filter(pump_name='Pump Three').last()
        serializers = PumpSerializer(pump_info,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class PumpFourInfo(APIView):
    permission_classes=(AllowAny,)
    def get_pump_info(self):
        try:
            return Pump.objects.all().filter(pump_name='Pump Four').last()
        except Pump.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        pump_info = Pump.objects.all().filter(pump_name='Pump Four').last()
        serializers = PumpSerializer(pump_info,many=False)
        return Response(serializers.data)

    def put(self, request, format=None):
        pump_info = Pump.objects.all().filter(pump_name='Pump Four').last()
        serializers = PumpSerializer(pump_info,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class AllLogs(APIView):
    permission_classes=(AllowAny,)
    def get_all_logs(self):
        try:
            return Log.objects.all()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        all_logs = Log.objects.all()
        serializers = LogSerializer(all_logs,many=True)
        return Response(serializers.data)

class TodayLogs(APIView):
    permission_classes=(AllowAny,)
    def get_today_logs(self):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today)
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        today_logs = Log.objects.all().filter(date=today)
        serializers = LogSerializer(today_logs,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = LogSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogs(APIView):
    permission_classes=(AllowAny,)
    def get_user_logs(self,id):
        try:
            return Log.objects.all().filter(user_id=id).order_by('-date')
        except Log.DoesNotExist:
            return Http404

    def get(self, request, id, format=None):
        user_logs = Log.objects.all().filter(user_id=id).order_by('-date')
        serializers = LogSerializer(user_logs,many=True)
        return Response(serializers.data)

class PetrolSummaryToday(APIView):
    permission_classes=(AllowAny,)
    def get_today_fuel_logs(self):
        today = dt.date.today()
        try:
            petrol_info = Fuel.objects.all().filter(fuel_type='Petrol').first()
            petrol_id = petrol_info.id
            return Fuel.objects.all().filter(fuel_id=petrol_id).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        yesterday = today - dt.timedelta(days=1)
        pump_one = Pump.objects.all().filter(pump_name='Pump One').first()
        pump_two = Pump.objects.all().filter(pump_name='Pump Two').first()
        pump_three = Pump.objects.all().filter(pump_name='Pump Three').first()
        pump_four = Pump.objects.all().filter(pump_name='Pump Four').first()
        petrol_info = Fuel.objects.all().filter(fuel_type='Petrol').first()
        today_petrol_info = Fuel.objects.all().filter(fuel_type='Petrol').filter(date=today).last()
        yesterday_petrol_info = Fuel.objects.all().filter(fuel_type='Petrol').filter(date=yesterday).last()
        if petrol_info:
            petrol_id = petrol_info.id 
        else:
            Http404

        if pump_one:
            pump_one_id = pump_one.id
        else:
            Http404
        if pump_two:
            pump_two_id = pump_two.id
        else:
            Http404
        if pump_three:
            pump_three_id = pump_three.id
        else:
            Http404
        if pump_four:
            pump_four_id = pump_four.id
        else:
            Http404
        today_fuel_log = Log.objects.all().filter(date=today).filter(fuel_id=petrol_id).filter(pump_id=pump_one_id).first()
        today_log_two = Log.objects.all().filter(date=today).filter(fuel_id=petrol_id).filter(pump_id=pump_two_id).first()
        today_log_three = Log.objects.all().filter(date=today).filter(fuel_id=petrol_id).filter(pump_id=pump_three_id).first()
        today_log_four = Log.objects.all().filter(date=today).filter(fuel_id=petrol_id).filter(pump_id=pump_four_id).first()
        petrol_received = FuelReceived.objects.all().filter(fuel_id=petrol_id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        if today_fuel_log and today_log_two and today_log_three and today_log_four and petrol_info:
            petrol_id = petrol_info.id
            petrol_received = FuelReceived.objects.all().filter(date_received=today).filter(fuel_id=petrol_id).last()
            total_one = today_fuel_log.total_litres_sold 
            total_two = today_log_two.total_litres_sold
            total_three = today_log_three.total_litres_sold 
            total_four = today_log_four.total_litres_sold 
            petrol_info.total_litres_sold_today = (total_one) + (total_two) + (total_three) + (total_four)
            petrol_info.save()
            petrol_info.refresh_from_db()
            amount_one = today_fuel_log.amount_earned_today 
            amount_two = today_log_two.amount_earned_today
            amount_three = today_log_three.amount_earned_today 
            amount_four = today_log_four.amount_earned_today 
            petrol_info.amount_earned_today = (amount_one) + (amount_two) + (amount_three) + (amount_four)
            petrol_info.save()
            petrol_info.refresh_from_db()
            if yesterday_petrol_info and petrol_info.total_litres_sold_today:
                petrol_info.balance_yesterday = yesterday_petrol_info.balance 
                petrol_info.save()
                petrol_info.refresh_from_db()
                bal_yesterday = petrol_info.balance_yesterday
                petrol_info.balance = (bal_yesterday) - (total_sold)
                petrol_info.save()
                petrol_info.refresh_from_db()
                bal = petrol_info.balance 
            elif petrol_info.balance_yesterday and petrol_info.total_litres_sold_today:
                bal_yesterday = petrol_info.balance_yesterday
                total_sold = petrol_info.total_litres_sold_today
                petrol_info.balance = (bal_yesterday) - (total_sold)
                petrol_info.save()
                petrol_info.refresh_from_db()
                bal = petrol_info.balance 
            elif petrol_info.total_litres_sold_today:
                init = petrol_info.initial_litres_in_tank 
                total_sold = petrol_info.total_litres_sold_today
                petrol_info.balance = (init) - (total_sold)
                petrol_info.save()
                petrol_info.refresh_from_db()
                    
                if petrol_info.balance and petrol_received.litres_received:
                    petrol_received = petrol_received.litres_received
                    bal = petrol_info.balance
                    petrol_info.updated_balance = (bal) + (petrol_received)
                    petrol_info.save()
                    petrol_info.refresh_from_db()
                    updated_bal = petrol_info.updated_balance 
                elif updated_bal and petrol_received:
                    petrol_info.updated_balance = (updated_bal) + (petrol_received)
                    petrol_info.save()
                    petrol_info.refresh_from_db()

        elif today_fuel_log and today_log_two and today_log_three and petrol_info:
            total_one = today_fuel_log.total_litres_sold 
            total_two = today_log_two.total_litres_sold 
            total_three = today_log_three.total_litres_sold 
            petrol_info.total_litres_sold_today = (total_one) + (total_two) + (total_three)
            petrol_info.save()
            petrol_info.refresh_from_db()
            amount_one = today_fuel_log.amount_earned_today 
            amount_two = today_log_two.amount_earned_today 
            amount_three = today_log_three.amount_earned_today 
            petrol_info.amount_earned_today = (amount_one) + (amount_two) + (amount_three)
            petrol_info.save()
            petrol_info.refresh_from_db()
            if yesterday_petrol_info and petrol_info.total_litres_sold_today:
                petrol_info.balance_yesterday = yesterday_petrol_info.balance 
                petrol_info.save()
                petrol_info.refresh_from_db()
                bal_yesterday = petrol_info.balance_yesterday
                petrol_info.balance = (bal_yesterday) - (total_sold)
                petrol_info.save()
                petrol_info.refresh_from_db()
                bal = petrol_info.balance 
            elif petrol_info.balance_yesterday and petrol_info.total_litres_sold_today:
                bal_yesterday = petrol_info.balance_yesterday
                total_sold = petrol_info.total_litres_sold_today
                petrol_info.balance = (bal_yesterday) - (total_sold)
                petrol_info.save()
                petrol_info.refresh_from_db()
                bal = petrol_info.balance 
            elif petrol_info.total_litres_sold_today:
                init = petrol_info.initial_litres_in_tank 
                total_sold = petrol_info.total_litres_sold_today
                petrol_info.balance = (init) - (total_sold)
                petrol_info.save()
                petrol_info.refresh_from_db()
                bal = petrol_info.balance
                if bal and petrol_received:
                    petrol_info.updated_balance = (bal) + (petrol_received)
                    petrol_info.save()
                    petrol_info.refresh_from_db()
                    updated_bal = petrol_info.updated_balance 
                elif updated_bal and petrol_received:
                    petrol_info.updated_balance = (updated_bal) + (petrol_received)
                    petrol_info.save()
                    petrol_info.refresh_from_db()
        elif today_fuel_log and today_log_two and petrol_info:
            total_one = today_fuel_log.total_litres_sold 
            total_two = today_log_two.total_litres_sold 
            petrol_info.total_litres_sold_today = (total_one) + (total_two)
            petrol_info.save()
            petrol_info.refresh_from_db()
            amount_one = today_fuel_log.amount_earned_today 
            amount_two = today_log_two.amount_earned_today 
            petrol_info.amount_earned_today = (amount_one) + (amount_two)
            petrol_info.save()
            petrol_info.refresh_from_db()
            if yesterday_petrol_info and petrol_info.total_litres_sold_today:
                petrol_info.balance_yesterday = yesterday_petrol_info.balance 
                petrol_info.save()
                petrol_info.refresh_from_db()
                bal_yesterday = petrol_info.balance_yesterday
                petrol_info.balance = (bal_yesterday) - (total_sold)
                petrol_info.save()
                petrol_info.refresh_from_db()
                bal = petrol_info.balance 
            elif petrol_info.balance_yesterday and petrol_info.total_litres_sold_today:
                bal_yesterday = petrol_info.balance_yesterday
                total_sold = petrol_info.total_litres_sold_today
                petrol_info.balance = (bal_yesterday) - (total_sold)
                petrol_info.save()
                petrol_info.refresh_from_db()
                bal = petrol_info.balance 
            elif petrol_info.total_litres_sold_today:
                init = petrol_info.initial_litres_in_tank 
                total_sold = petrol_info.total_litres_sold_today
                petrol_info.balance = (init) - (total_sold)
                petrol_info.save()
                petrol_info.refresh_from_db()
                bal = petrol_info.balance
                if bal and petrol_received:
                    petrol_info.updated_balance = (bal) + (petrol_received)
                    petrol_info.save()
                    petrol_info.refresh_from_db()
                    updated_bal = petrol_info.updated_balance 
                elif updated_bal and petrol_received:
                    petrol_info.updated_balance = (updated_bal) + (petrol_received)
                    petrol_info.save()
                    petrol_info.refresh_from_db()
        elif today_fuel_log and petrol_info:
            total_one = today_fuel_log.total_litres_sold 
            print("total one:",total_one)
            petrol_info.total_litres_sold_today = total_one
            petrol_info.save()
            petrol_info.refresh_from_db()
            amount_one = today_fuel_log.amount_earned_today 
            petrol_info.amount_earned_today = amount_one
            petrol_info.save()
            petrol_info.refresh_from_db()
            if yesterday_petrol_info and petrol_info.total_litres_sold_today:
                petrol_info.balance_yesterday = yesterday_petrol_info.balance 
                petrol_info.save()
                petrol_info.refresh_from_db()
                bal_yesterday = petrol_info.balance_yesterday
                petrol_info.balance = (bal_yesterday) - (total_sold)
                petrol_info.save()
                petrol_info.refresh_from_db()
                bal = petrol_info.balance 
            elif petrol_info.balance_yesterday and petrol_info.total_litres_sold_today:
                bal_yesterday = petrol_info.balance_yesterday
                total_sold = petrol_info.total_litres_sold_today
                petrol_info.balance = (bal_yesterday) - (total_sold)
                petrol_info.save()
                petrol_info.refresh_from_db()
                bal = petrol_info.balance 
            elif petrol_info.total_litres_sold_today:
                init = petrol_info.initial_litres_in_tank 
                total_sold = petrol_info.total_litres_sold_today
                petrol_info.balance = (init) - (total_sold)
                petrol_info.save()
                petrol_info.refresh_from_db()
                bal = petrol_info.balance
                if bal and petrol_received:
                    petrol_info.updated_balance = (bal) + (petrol_received)
                    petrol_info.save()
                    petrol_info.refresh_from_db()
                    updated_bal = petrol_info.updated_balance 
                elif updated_bal and petrol_received:
                    petrol_info.updated_balance = (updated_bal) + (petrol_received)
                    petrol_info.save()
                    petrol_info.refresh_from_db()
        serializers = FuelSerializer(petrol_info,many=False)
        return Response(serializers.data)


class DieselSummaryToday(APIView):
    permission_classes=(AllowAny,)
    def get_today_fuel_logs(self):
        today = dt.date.today()
        try:
            diesel_info = Fuel.objects.all().filter(fuel_type='Diesel').first()
            diesel_id = diesel_info.id
            return Fuel.objects.all().filter(fuel_id=diesel_id).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        yesterday = today - dt.timedelta(days=1)
        pump_one = Pump.objects.all().filter(pump_name='Pump One').first()
        pump_two = Pump.objects.all().filter(pump_name='Pump Two').first()
        pump_three = Pump.objects.all().filter(pump_name='Pump Three').first()
        pump_four = Pump.objects.all().filter(pump_name='Pump Four').first()
        diesel_info = Fuel.objects.all().filter(fuel_type='Diesel').first()
        today_diesel_info = Fuel.objects.all().filter(fuel_type='Diesel').filter(date=today).last()
        yesterday_diesel_info = Fuel.objects.all().filter(fuel_type='Diesel').filter(date=yesterday).last()
        
        if diesel_info:
            diesel_id = diesel_info.id 
        else:
            Http404

        if pump_one:
            pump_one_id = pump_one.id
        else:
            Http404
        if pump_two:
            pump_two_id = pump_two.id
        else:
            Http404
        if pump_three:
            pump_three_id = pump_three.id
        else:
            Http404
        if pump_four:
            pump_four_id = pump_four.id
        else:
            Http404
        today_fuel_log = Log.objects.all().filter(date=today).filter(fuel_id=diesel_id).filter(pump_id=pump_one_id).first()
        today_log_two = Log.objects.all().filter(date=today).filter(fuel_id=diesel_id).filter(pump_id=pump_two_id).first()
        today_log_three = Log.objects.all().filter(date=today).filter(fuel_id=diesel_id).filter(pump_id=pump_three_id).first()
        today_log_four = Log.objects.all().filter(date=today).filter(fuel_id=diesel_id).filter(pump_id=pump_four_id).first()
        diesel_received = FuelReceived.objects.all().filter(fuel_id=diesel_id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        if today_fuel_log and today_log_two and today_log_three and today_log_four and diesel_info:
            diesel_id = diesel_info.id
            diesel_received = FuelReceived.objects.all().filter(date_received=today).filter(fuel_id=diesel_id).last()
            total_one = today_fuel_log.total_litres_sold 
            total_two = today_log_two.total_litres_sold
            total_three = today_log_three.total_litres_sold 
            total_four = today_log_four.total_litres_sold 
            diesel_info.total_litres_sold_today = (total_one) + (total_two) + (total_three) + (total_four)
            diesel_info.save()
            diesel_info.refresh_from_db()
            amount_one = today_fuel_log.amount_earned_today 
            amount_two = today_log_two.amount_earned_today
            amount_three = today_log_three.amount_earned_today 
            amount_four = today_log_four.amount_earned_today 
            diesel_info.amount_earned_today = (amount_one) + (amount_two) + (amount_three) + (amount_four)
            diesel_info.save()
            diesel_info.refresh_from_db()
            if yesterday_diesel_info and diesel_info.total_litres_sold_today:
                diesel_info.balance_yesterday = yesterday_diesel_info.balance 
                diesel_info.save()
                diesel_info.refresh_from_db()
                bal_yesterday = diesel_info.balance_yesterday
                diesel_info.balance = (bal_yesterday) - (total_sold)
                diesel_info.save()
                diesel_info.refresh_from_db()
                bal = diesel_info.balance 
            elif diesel_info.balance_yesterday and diesel_info.total_litres_sold_today:
                bal_yesterday = diesel_info.balance_yesterday
                total_sold = diesel_info.total_litres_sold_today
                diesel_info.balance = (bal_yesterday) - (total_sold)
                diesel_info.save()
                diesel_info.refresh_from_db()
                bal = diesel_info.balance 
            elif diesel_info.total_litres_sold_today:
                init = diesel_info.initial_litres_in_tank 
                total_sold = diesel_info.total_litres_sold_today
                diesel_info.balance = (init) - (total_sold)
                diesel_info.save()
                diesel_info.refresh_from_db()
                    
                if diesel_info.balance and diesel_received.litres_received:
                    diesel_received = diesel_received.litres_received
                    bal = diesel_info.balance
                    diesel_info.updated_balance = (bal) + (diesel_received)
                    diesel_info.save()
                    diesel_info.refresh_from_db()
                    updated_bal = diesel_info.updated_balance 
                elif updated_bal and diesel_received:
                    diesel_info.updated_balance = (updated_bal) + (diesel_received)
                    diesel_info.save()
                    diesel_info.refresh_from_db()

        elif today_fuel_log and today_log_two and today_log_three and diesel_info:
            total_one = today_fuel_log.total_litres_sold 
            total_two = today_log_two.total_litres_sold 
            total_three = today_log_three.total_litres_sold 
            diesel_info.total_litres_sold_today = (total_one) + (total_two) + (total_three)
            diesel_info.save()
            diesel_info.refresh_from_db()
            amount_one = today_fuel_log.amount_earned_today 
            amount_two = today_log_two.amount_earned_today 
            amount_three = today_log_three.amount_earned_today 
            diesel_info.amount_earned_today = (amount_one) + (amount_two) + (amount_three)
            diesel_info.save()
            diesel_info.refresh_from_db()
            if yesterday_diesel_info and diesel_info.total_litres_sold_today:
                diesel_info.balance_yesterday = yesterday_diesel_info.balance 
                diesel_info.save()
                diesel_info.refresh_from_db()
                bal_yesterday = diesel_info.balance_yesterday
                diesel_info.balance = (bal_yesterday) - (total_sold)
                diesel_info.save()
                diesel_info.refresh_from_db()
                bal = diesel_info.balance 
            elif diesel_info.balance_yesterday and diesel_info.total_litres_sold_today:
                bal_yesterday = diesel_info.balance_yesterday
                total_sold = diesel_info.total_litres_sold_today
                diesel_info.balance = (bal_yesterday) - (total_sold)
                diesel_info.save()
                diesel_info.refresh_from_db()
                bal = diesel_info.balance 
            elif diesel_info.total_litres_sold_today:
                init = diesel_info.initial_litres_in_tank 
                total_sold = diesel_info.total_litres_sold_today
                diesel_info.balance = (init) - (total_sold)
                diesel_info.save()
                diesel_info.refresh_from_db()
                bal = diesel_info.balance
                if bal and diesel_received:
                    diesel_info.updated_balance = (bal) + (diesel_received)
                    diesel_info.save()
                    diesel_info.refresh_from_db()
                    updated_bal = diesel_info.updated_balance 
                elif updated_bal and diesel_received:
                    diesel_info.updated_balance = (updated_bal) + (diesel_received)
                    diesel_info.save()
                    diesel_info.refresh_from_db()
        elif today_fuel_log and today_log_two and diesel_info:
            total_one = today_fuel_log.total_litres_sold 
            total_two = today_log_two.total_litres_sold 
            diesel_info.total_litres_sold_today = (total_one) + (total_two)
            diesel_info.save()
            diesel_info.refresh_from_db()
            amount_one = today_fuel_log.amount_earned_today 
            amount_two = today_log_two.amount_earned_today 
            diesel_info.amount_earned_today = (amount_one) + (amount_two)
            diesel_info.save()
            diesel_info.refresh_from_db()
            if yesterday_diesel_info and diesel_info.total_litres_sold_today:
                diesel_info.balance_yesterday = yesterday_diesel_info.balance 
                diesel_info.save()
                diesel_info.refresh_from_db()
                bal_yesterday = diesel_info.balance_yesterday
                diesel_info.balance = (bal_yesterday) - (total_sold)
                diesel_info.save()
                diesel_info.refresh_from_db()
                bal = diesel_info.balance 
            elif diesel_info.balance_yesterday and diesel_info.total_litres_sold_today:
                bal_yesterday = diesel_info.balance_yesterday
                total_sold = diesel_info.total_litres_sold_today
                diesel_info.balance = (bal_yesterday) - (total_sold)
                diesel_info.save()
                diesel_info.refresh_from_db()
                bal = diesel_info.balance 
            elif diesel_info.total_litres_sold_today:
                init = diesel_info.initial_litres_in_tank 
                total_sold = diesel_info.total_litres_sold_today
                diesel_info.balance = (init) - (total_sold)
                diesel_info.save()
                diesel_info.refresh_from_db()
                bal = diesel_info.balance
                if bal and diesel_received:
                    diesel_info.updated_balance = (bal) + (diesel_received)
                    diesel_info.save()
                    diesel_info.refresh_from_db()
                    updated_bal = diesel_info.updated_balance 
                elif updated_bal and diesel_received:
                    diesel_info.updated_balance = (updated_bal) + (diesel_received)
                    diesel_info.save()
                    diesel_info.refresh_from_db()
        elif today_fuel_log and diesel_info:
            total_one = today_fuel_log.total_litres_sold 
            print("total one:",total_one)
            diesel_info.total_litres_sold_today = total_one
            diesel_info.save()
            diesel_info.refresh_from_db()
            amount_one = today_fuel_log.amount_earned_today 
            diesel_info.amount_earned_today = amount_one
            diesel_info.save()
            diesel_info.refresh_from_db()
            if yesterday_diesel_info and diesel_info.total_litres_sold_today:
                diesel_info.balance_yesterday = yesterday_diesel_info.balance 
                diesel_info.save()
                diesel_info.refresh_from_db()
                bal_yesterday = diesel_info.balance_yesterday
                diesel_info.balance = (bal_yesterday) - (total_sold)
                diesel_info.save()
                diesel_info.refresh_from_db()
                bal = diesel_info.balance 
            elif diesel_info.balance_yesterday and diesel_info.total_litres_sold_today:
                bal_yesterday = diesel_info.balance_yesterday
                total_sold = diesel_info.total_litres_sold_today
                diesel_info.balance = (bal_yesterday) - (total_sold)
                diesel_info.save()
                diesel_info.refresh_from_db()
                bal = diesel_info.balance 
            elif diesel_info.total_litres_sold_today:
                init = diesel_info.initial_litres_in_tank 
                total_sold = diesel_info.total_litres_sold_today
                diesel_info.balance = (init) - (total_sold)
                diesel_info.save()
                diesel_info.refresh_from_db()
                bal = diesel_info.balance
                if bal and diesel_received:
                    diesel_info.updated_balance = (bal) + (diesel_received)
                    diesel_info.save()
                    diesel_info.refresh_from_db()
                    updated_bal = diesel_info.updated_balance 
                elif updated_bal and diesel_received:
                    diesel_info.updated_balance = (updated_bal) + (diesel_received)
                    diesel_info.save()
                    diesel_info.refresh_from_db()
        serializers = FuelSerializer(diesel_info,many=False)
        return Response(serializers.data)


class GasSummaryToday(APIView):
    permission_classes=(AllowAny,)
    def get_today_fuel_logs(self):
        today = dt.date.today()
        try:
            gas_info = Fuel.objects.all().filter(fuel_type='Gas').first()
            gas_id = gas_info.id
            return Fuel.objects.all().filter(fuel_id=gas_id).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        yesterday = today - dt.timedelta(days=1)
        pump_one = Pump.objects.all().filter(pump_name='Pump One').first()
        pump_two = Pump.objects.all().filter(pump_name='Pump Two').first()
        pump_three = Pump.objects.all().filter(pump_name='Pump Three').first()
        pump_four = Pump.objects.all().filter(pump_name='Pump Four').first()
        gas_info = Fuel.objects.all().filter(fuel_type='Gas').first()
        today_gas_info = Fuel.objects.all().filter(fuel_type='Gas').filter(date=today).last()
        yesterday_gas_info = Fuel.objects.all().filter(fuel_type='Gas').filter(date=yesterday).last()
        if gas_info:
            gas_id = gas_info.id 
        else:
            Http404

        if pump_one:
            pump_one_id = pump_one.id
        else:
            Http404
        if pump_two:
            pump_two_id = pump_two.id
        else:
            Http404
        if pump_three:
            pump_three_id = pump_three.id
        else:
            Http404
        if pump_four:
            pump_four_id = pump_four.id
        else:
            Http404
        today_fuel_log = Log.objects.all().filter(date=today).filter(fuel_id=gas_id).filter(pump_id=pump_one_id).first()
        today_log_two = Log.objects.all().filter(date=today).filter(fuel_id=gas_id).filter(pump_id=pump_two_id).first()
        today_log_three = Log.objects.all().filter(date=today).filter(fuel_id=gas_id).filter(pump_id=pump_three_id).first()
        today_log_four = Log.objects.all().filter(date=today).filter(fuel_id=gas_id).filter(pump_id=pump_four_id).first()
        gas_received = FuelReceived.objects.all().filter(fuel_id=gas_id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        if today_fuel_log and today_log_two and today_log_three and today_log_four and gas_info:
            gas_id = gas_info.id
            gas_received = FuelReceived.objects.all().filter(date_received=today).filter(fuel_id=gas_id).last()
            total_one = today_fuel_log.total_litres_sold 
            total_two = today_log_two.total_litres_sold
            total_three = today_log_three.total_litres_sold 
            total_four = today_log_four.total_litres_sold 
            gas_info.total_litres_sold_today = (total_one) + (total_two) + (total_three) + (total_four)
            gas_info.save()
            gas_info.refresh_from_db()
            amount_one = today_fuel_log.amount_earned_today 
            amount_two = today_log_two.amount_earned_today
            amount_three = today_log_three.amount_earned_today 
            amount_four = today_log_four.amount_earned_today 
            gas_info.amount_earned_today = (amount_one) + (amount_two) + (amount_three) + (amount_four)
            gas_info.save()
            gas_info.refresh_from_db()
            if yesterday_gas_info and gas_info.total_litres_sold_today:
                gas_info.balance_yesterday = yesterday_gas_info.balance 
                gas_info.save()
                gas_info.refresh_from_db()
                bal_yesterday = gas_info.balance_yesterday
                gas_info.balance = (bal_yesterday) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance 
            elif gas_info.balance_yesterday and gas_info.total_litres_sold_today:
                bal_yesterday = gas_info.balance_yesterday
                total_sold = gas_info.total_litres_sold_today
                gas_info.balance = (bal_yesterday) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance 
            elif gas_info.total_litres_sold_today:
                init = gas_info.initial_litres_in_tank 
                total_sold = gas_info.total_litres_sold_today
                gas_info.balance = (init) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                    
                if gas_info.balance and gas_received.litres_received:
                    gas_received = gas_received.litres_received
                    bal = gas_info.balance
                    gas_info.updated_balance = (bal) + (gas_received)
                    gas_info.save()
                    gas_info.refresh_from_db()
                    updated_bal = gas_info.updated_balance 
                elif updated_bal and gas_received:
                    gas_info.updated_balance = (updated_bal) + (gas_received)
                    gas_info.save()
                    gas_info.refresh_from_db()

        elif today_fuel_log and today_log_two and today_log_three and gas_info:
            total_one = today_fuel_log.total_litres_sold 
            total_two = today_log_two.total_litres_sold 
            total_three = today_log_three.total_litres_sold 
            gas_info.total_litres_sold_today = (total_one) + (total_two) + (total_three)
            gas_info.save()
            gas_info.refresh_from_db()
            amount_one = today_fuel_log.amount_earned_today 
            amount_two = today_log_two.amount_earned_today 
            amount_three = today_log_three.amount_earned_today 
            gas_info.amount_earned_today = (amount_one) + (amount_two) + (amount_three)
            gas_info.save()
            gas_info.refresh_from_db()
            if yesterday_gas_info and gas_info.total_litres_sold_today:
                gas_info.balance_yesterday = yesterday_gas_info.balance 
                gas_info.save()
                gas_info.refresh_from_db()
                bal_yesterday = gas_info.balance_yesterday
                gas_info.balance = (bal_yesterday) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance 
            elif gas_info.balance_yesterday and gas_info.total_litres_sold_today:
                bal_yesterday = gas_info.balance_yesterday
                total_sold = gas_info.total_litres_sold_today
                gas_info.balance = (bal_yesterday) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance 
            elif gas_info.total_litres_sold_today:
                init = gas_info.initial_litres_in_tank 
                total_sold = gas_info.total_litres_sold_today
                gas_info.balance = (init) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance
                if bal and gas_received:
                    gas_info.updated_balance = (bal) + (gas_received)
                    gas_info.save()
                    gas_info.refresh_from_db()
                    updated_bal = gas_info.updated_balance 
                elif updated_bal and gas_received:
                    gas_info.updated_balance = (updated_bal) + (gas_received)
                    gas_info.save()
                    gas_info.refresh_from_db()
        elif today_fuel_log and today_log_two and gas_info:
            total_one = today_fuel_log.total_litres_sold 
            total_two = today_log_two.total_litres_sold 
            gas_info.total_litres_sold_today = (total_one) + (total_two)
            gas_info.save()
            gas_info.refresh_from_db()
            amount_one = today_fuel_log.amount_earned_today 
            amount_two = today_log_two.amount_earned_today 
            gas_info.amount_earned_today = (amount_one) + (amount_two)
            gas_info.save()
            gas_info.refresh_from_db()
            if yesterday_gas_info and gas_info.total_litres_sold_today:
                gas_info.balance_yesterday = yesterday_gas_info.balance 
                gas_info.save()
                gas_info.refresh_from_db()
                bal_yesterday = gas_info.balance_yesterday
                gas_info.balance = (bal_yesterday) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance 
            elif gas_info.balance_yesterday and gas_info.total_litres_sold_today:
                bal_yesterday = gas_info.balance_yesterday
                total_sold = gas_info.total_litres_sold_today
                gas_info.balance = (bal_yesterday) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance 
            elif gas_info.total_litres_sold_today:
                init = gas_info.initial_litres_in_tank 
                total_sold = gas_info.total_litres_sold_today
                gas_info.balance = (init) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance
                if bal and gas_received:
                    gas_info.updated_balance = (bal) + (gas_received)
                    gas_info.save()
                    gas_info.refresh_from_db()
                    updated_bal = gas_info.updated_balance 
                elif updated_bal and gas_received:
                    gas_info.updated_balance = (updated_bal) + (gas_received)
                    gas_info.save()
                    gas_info.refresh_from_db()
        elif today_fuel_log and gas_info:
            total_one = today_fuel_log.total_litres_sold 
            print("total one:",total_one)
            gas_info.total_litres_sold_today = total_one
            gas_info.save()
            gas_info.refresh_from_db()
            amount_one = today_fuel_log.amount_earned_today 
            gas_info.amount_earned_today = amount_one
            gas_info.save()
            gas_info.refresh_from_db()
            if yesterday_gas_info and gas_info.total_litres_sold_today:
                gas_info.balance_yesterday = yesterday_gas_info.balance 
                gas_info.save()
                gas_info.refresh_from_db()
                bal_yesterday = gas_info.balance_yesterday
                gas_info.balance = (bal_yesterday) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance 
            elif gas_info.balance_yesterday and gas_info.total_litres_sold_today:
                bal_yesterday = gas_info.balance_yesterday
                total_sold = gas_info.total_litres_sold_today
                gas_info.balance = (bal_yesterday) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance 
            elif gas_info.total_litres_sold_today:
                init = gas_info.initial_litres_in_tank 
                total_sold = gas_info.total_litres_sold_today
                gas_info.balance = (init) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance
                if bal and gas_received:
                    gas_info.updated_balance = (bal) + (gas_received)
                    gas_info.save()
                    gas_info.refresh_from_db()
                    updated_bal = gas_info.updated_balance 
                elif updated_bal and gas_received:
                    gas_info.updated_balance = (updated_bal) + (gas_received)
                    gas_info.save()
                    gas_info.refresh_from_db()
        serializers = FuelSerializer(gas_info,many=False)
        return Response(serializers.data)


class TodayFuelLogs(APIView):
    permission_classes=(AllowAny,)
    def get_today_fuel_logs(self,id):
        today = dt.date.today()
        try:
            pump_one = Pump.objects.all().filter(pump_name='Pump One').first()
            pump_one_id = pump_one.id
            return Log.objects.all().filter(date=today).filter(fuel_id=id).filter(pump_id=pump_one_id).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, id, format=None):
        today = dt.date.today()
        pump_one = Pump.objects.all().filter(pump_name='Pump One').first()
        pump_one_id = pump_one.id
        today_fuel_log = Log.objects.all().filter(date=today).filter(fuel_id=id).filter(pump_id=pump_one_id).first()
        fuel_received = FuelReceived.objects.all().filter(fuel_id=id).filter(pump_id=pump_one_id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        yesterday = today - dt.timedelta(days=1)
        yesterday_fuel_logs = Log.objects.all().filter(fuel_id=id).filter(pump_id=pump_one_id).filter(date=yesterday).first()
        fuel_info = Fuel.objects.all().filter(id=id).last()
        if today_fuel_log and fuel_info:
            price_per_litre = fuel_info.price_per_litre 
            init = fuel_info.initial_litres_in_tank
            today_fuel_log.fuel_name = today_fuel_log.fuel.fuel_type
            today_fuel_log.save()
            today_fuel_log.refresh_from_db()
            today_fuel_log.pump_name = today_fuel_log.pump.pump_name
            today_fuel_log.save()
            today_fuel_log.refresh_from_db()
            if yesterday_fuel_logs:
                eod_yesterday = yesterday_fuel_logs.eod_reading_lts
                today_fuel_log.eod_reading_yesterday = eod_yesterday
                today_fuel_log.save()
                today_fuel_log.refresh_from_db()
                today_fuel_log.total_litres_sold = ExpressionWrapper(F('eod_reading_lts')-F('eod_reading_yesterday'),output_field=DecimalField())
                today_fuel_log.save()
                today_fuel_log.refresh_from_db()
                today_fuel_log.amount_earned_today = ExpressionWrapper(F('total_litres_sold') * (price_per_litre),output_field=PositiveIntegerField())
                today_fuel_log.save()
                today_fuel_log.refresh_from_db()
            else:
                today_fuel_log.total_litres_sold = ExpressionWrapper(F('eod_reading_lts')-F('eod_reading_yesterday'),output_field=DecimalField())
                today_fuel_log.save()
                today_fuel_log.refresh_from_db()
                today_fuel_log.amount_earned_today = ExpressionWrapper(F('total_litres_sold') * (price_per_litre),output_field=PositiveIntegerField())
                today_fuel_log.save()
                today_fuel_log.refresh_from_db()
        else: 
            Http404
        serializers = LogSerializer(today_fuel_log,many=False)
        return Response(serializers.data)

class TodayFuelLogsTwo(APIView):
    permission_classes=(AllowAny,)
    def get_today_fuel_logs_two(self,id):
        today = dt.date.today()
        pump_two = Pump.objects.all().filter(pump_name='Pump Two').first()
        pump_two_id = pump_two.id
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=id).filter(pump_id=pump_two_id).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, id, format=None):
        pump_two = Pump.objects.all().filter(pump_name='Pump Two').first()
        pump_two_id = pump_two.id
        today = dt.date.today()
        today_log_two = Log.objects.all().filter(date=today).filter(fuel_id=id).filter(pump_id=pump_two_id).first()
        fuel_received = FuelReceived.objects.all().filter(fuel_id=id).filter(pump_id=pump_two_id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        yesterday = today - dt.timedelta(days=1)
        yesterday_log_two = Log.objects.all().filter(fuel_id=id).filter(date=yesterday).filter(pump_id=pump_two_id).first()
        fuel_info = Fuel.objects.all().filter(id=id).last()
        if today_log_two and fuel_info:
            price_per_litre = fuel_info.price_per_litre 
            init = fuel_info.initial_litres_in_tank
            today_log_two.fuel_name = today_log_two.fuel.fuel_type
            today_log_two.save()
            today_log_two.refresh_from_db()
            today_log_two.pump_name = today_log_two.pump.pump_name
            today_log_two.save()
            today_log_two.refresh_from_db()
            if yesterday_log_two:
                eod_yesterday = yesterday_log_two.eod_reading_lts
                today_log_two.eod_reading_yesterday = eod_yesterday
                today_log_two.save()
                today_log_two.refresh_from_db()
                today_log_two.total_litres_sold = ExpressionWrapper(F('eod_reading_lts')-F('eod_reading_yesterday'),output_field=DecimalField())
                today_log_two.save()
                today_log_two.refresh_from_db()
                today_log_two.amount_earned_today = ExpressionWrapper(F('total_litres_sold') * (price_per_litre),output_field=PositiveIntegerField())
                today_log_two.save()
                today_log_two.refresh_from_db()
            else:
                today_log_two.total_litres_sold = ExpressionWrapper(F('eod_reading_lts')-F('eod_reading_yesterday'),output_field=DecimalField())
                today_log_two.save()
                today_log_two.refresh_from_db()
                today_log_two.amount_earned_today = ExpressionWrapper(F('total_litres_sold') * (price_per_litre),output_field=PositiveIntegerField())
                today_log_two.save()
                today_log_two.refresh_from_db()
        else: 
            Http404
        serializers = LogSerializer(today_log_two,many=False)
        return Response(serializers.data)

class TodayFuelLogsThree(APIView):
    permission_classes=(AllowAny,)
    def get_today_fuel_logs_three(self,id):
        today = dt.date.today()
        pump_three = Pump.objects.all().filter(pump_name='Pump Three').first()
        pump_three_id = pump_three.id
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=id).filter(pump_id=pump_three_id).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, id, format=None):
        today = dt.date.today()
        pump_three = Pump.objects.all().filter(pump_name='Pump Three').first()
        pump_three_id = pump_three.id
        today_log_three = Log.objects.all().filter(date=today).filter(fuel_id=id).filter(pump_id=pump_three_id).first()
        fuel_received = FuelReceived.objects.all().filter(fuel_id=id).filter(pump_id=pump_three_id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        yesterday = today - dt.timedelta(days=1)
        yesterday_log_three = Log.objects.all().filter(fuel_id=id).filter(date=yesterday).filter(pump_id=pump_three_id).first()
        fuel_info = Fuel.objects.all().filter(id=id).last()
        if today_log_three and fuel_info:
            price_per_litre = fuel_info.price_per_litre 
            init = fuel_info.initial_litres_in_tank
            today_log_three.fuel_name = today_log_three.fuel.fuel_type
            today_log_three.save()
            today_log_three.refresh_from_db()
            today_log_three.pump_name = today_log_three.pump.pump_name
            today_log_three.save()
            today_log_three.refresh_from_db()
            if yesterday_log_three:
                eod_yesterday = yesterday_log_three.eod_reading_lts
                today_log_three.eod_reading_yesterday = eod_yesterday
                today_log_three.save()
                today_log_three.refresh_from_db()
                today_log_three.total_litres_sold = ExpressionWrapper(F('eod_reading_lts')-F('eod_reading_yesterday'),output_field=DecimalField())
                today_log_three.save()
                today_log_three.refresh_from_db()
                today_log_three.amount_earned_today = ExpressionWrapper(F('total_litres_sold') * (price_per_litre),output_field=PositiveIntegerField())
                today_log_three.save()
                today_log_three.refresh_from_db()
            else:
                today_log_three.total_litres_sold = ExpressionWrapper(F('eod_reading_lts')-F('eod_reading_yesterday'),output_field=DecimalField())
                today_log_three.save()
                today_log_three.refresh_from_db()
                today_log_three.amount_earned_today = ExpressionWrapper(F('total_litres_sold') * (price_per_litre),output_field=PositiveIntegerField())
                today_log_three.save()
                today_log_three.refresh_from_db()
        else: 
            Http404
        serializers = LogSerializer(today_log_three,many=False)
        return Response(serializers.data)

class TodayFuelLogsFour(APIView):
    permission_classes=(AllowAny,)
    def get_today_fuel_logs_four(self, id):
        today = dt.date.today()
        pump_four = Pump.objects.all().filter(pump_name='Pump Three').first()
        pump_four_id = pump_four.id
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=id).filter(pump_id=pump_four_id).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, id, format=None):
        today = dt.date.today()
        pump_four = Pump.objects.all().filter(pump_name='Pump Three').first()
        pump_four_id = pump_four.id
        today_log_four = Log.objects.all().filter(date=today).filter(fuel_id=id).filter(pump_id=pump_four_id).first()
        fuel_received = FuelReceived.objects.all().filter(fuel_id=id).filter(pump_id=pump_four_id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        yesterday = today - dt.timedelta(days=1)
        yesterday_log_four = Log.objects.all().filter(fuel_id=id).filter(date=yesterday).filter(pump_id=pump_four_id).first()
        fuel_info = Fuel.objects.all().filter(id=id).last()
        if today_log_four and fuel_info:
            price_per_litre = fuel_info.price_per_litre 
            init = fuel_info.initial_litres_in_tank
            today_log_four.fuel_name = today_log_four.fuel.fuel_type
            today_log_four.save()
            today_log_four.refresh_from_db()
            today_log_four.pump_name = today_log_four.pump.pump_name
            today_log_four.save()
            today_log_four.refresh_from_db()
            if yesterday_log_four:
                eod_yesterday = yesterday_log_four.eod_reading_lts
                today_log_four.eod_reading_yesterday = eod_yesterday
                today_log_four.save()
                today_log_four.refresh_from_db()
                today_log_four.total_litres_sold = ExpressionWrapper(F('eod_reading_lts')-F('eod_reading_yesterday'),output_field=DecimalField())
                today_log_four.save()
                today_log_four.refresh_from_db()
                today_log_four.amount_earned_today = ExpressionWrapper(F('total_litres_sold') * (price_per_litre),output_field=PositiveIntegerField())
                today_log_four.save()
                today_log_four.refresh_from_db()
            else:
                today_log_four.total_litres_sold = ExpressionWrapper(F('eod_reading_lts')-F('eod_reading_yesterday'),output_field=DecimalField())
                today_log_four.save()
                today_log_four.refresh_from_db()
                today_log_four.amount_earned_today = ExpressionWrapper(F('total_litres_sold') * (price_per_litre),output_field=PositiveIntegerField())
                today_log_four.save()
                today_log_four.refresh_from_db()
        else: 
            Http404
        serializers = LogSerializer(today_log_four,many=False)
        return Response(serializers.data)

class AllMpesaLogs(APIView):
    permission_classes=(AllowAny,)
    def get_all_mpesa_logs(self):
        try:
            return LogMpesa.objects.all()
        except LogMpesa.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        all_mpesa_logs = LogMpesa.objects.all()
        serializers = LogMpesaSerializer(all_mpesa_logs,many=True)
        return Response(serializers.data)

class TodayMpesaLogs(APIView):
    permission_classes=(AllowAny,)
    def get_today_mpesa_logs(self):
        today = dt.date.today()
        try:
            return LogMpesa.objects.all().filter(date=today)
        except LogMpesa.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        today_mpesa_logs = LogMpesa.objects.all().filter(date=today)
        serializers = LogMpesaSerializer(today_mpesa_logs,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = LogMpesaSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class UserMpesaLogs(APIView):
    permission_classes=(AllowAny,)
    def get_user_mpesa_logs(self,id):
        try:
            return LogMpesa.objects.all().filter(user=id).order_by('-date')
        except LogMpesa.DoesNotExist:
            return Http404

    def get(self, request, id, format=None):
        user_mpesa_logs = LogMpesa.objects.all().filter(user=id).order_by('-date')
        serializers = LogMpesaSerializer(user_mpesa_logs,many=True)
        return Response(serializers.data)

class AllFuelReceivedToday(APIView):
    permission_classes=(AllowAny,)
    def get_fuel_received(self):
        today = dt.date.today()
        try:
            return FuelReceived.objects.all().filter(date_received=today)
        except FuelReceived.DoesNotExist:
            return Http404
    
    def get(self, request, format=None):
        today = dt.date.today()
        fuel_received_today = FuelReceived.objects.all().filter(date_received=today)
        serializers = FuelReceivedSerializer(fuel_received_today,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = FuelReceivedSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class PetrolReceivedTodayInfo(APIView):
    permission_classes=(AllowAny,)
    def get_fuel_received_info(self,id):
        petrol_info = Fuel.objects.all().filter(fuel_type='Petrol').last()
        if petrol_info:
            petrol_id = petrol_info.id
        else:
            Http404
        log_details = Log.objects.all().filter(id=id).filter(fuel_id=petrol_id).first() 
        if log_details:
            log_date = log_details.date
            try:
                return FuelReceived.objects.all().filter(fuel_id=petrol_id).filter(date_received=log_date)
            except FuelReceived.DoesNotExist:
                return Http404
        else:
            Http404
    
    def get(self, request, id, format=None):
        today = dt.date.today()
        petrol_info = Fuel.objects.all().filter(fuel_type='Petrol').last()
        if petrol_info:
            print(petrol_info)
            print(petrol_info.id)
            petrol_id = petrol_info.id
        else:
            Http404
        log_details = Log.objects.all().filter(id=id).filter(fuel_id=petrol_id).first() 
        if log_details:
            log_date = log_details.date
            petrol_received_info = FuelReceived.objects.all().filter(fuel_id=petrol_id).last()
            if petrol_received_info:
                petrol_received_info.total_fuel_received_today = FuelReceived.objects.all().filter(fuel_id=petrol_id).filter(date_received=log_date).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
                petrol_received_info.fuel_name = petrol_received_info.fuel.fuel_type
                petrol_received_info.save()
                petrol_received_info.refresh_from_db()
            fuel_received_info = FuelReceived.objects.all().filter(fuel_id=petrol_id).filter(date_received=log_date)
        serializers = FuelReceivedSerializer(fuel_received_info,many=True)
        return Response(serializers.data)


class DieselReceivedTodayInfo(APIView):
    permission_classes=(AllowAny,)
    def get_fuel_received_info(self,id):
        diesel_info = Fuel.objects.all().filter(fuel_type='Diesel').last()
        if diesel_info:
            print(diesel_info)
            print(diesel_info.id)
            diesel_id = diesel_info.id
        else:
            Http404
        log_details = Log.objects.all().filter(id=id).filter(fuel_id=diesel_id).first() 
        if log_details:
            log_date = log_details.date
            try:
                return FuelReceived.objects.all().filter(fuel_id=diesel_id).filter(date_received=log_date)
            except FuelReceived.DoesNotExist:
                return Http404
        else:
            Http404
    
    def get(self, request, id, format=None):
        today = dt.date.today()
        diesel_info = Fuel.objects.all().filter(fuel_type='Diesel').last()
        if diesel_info:
            print(diesel_info)
            print(diesel_info.id)
            diesel_id = diesel_info.id
        else:
            Http404
        log_details = Log.objects.all().filter(id=id).filter(fuel_id=diesel_id).first() 
        if log_details:
            log_date = log_details.date
            diesel_received_info = FuelReceived.objects.all().filter(fuel_id=diesel_id).last()
            if diesel_received_info:
                diesel_received_info.total_fuel_received_today = FuelReceived.objects.all().filter(fuel_id=diesel_id).filter(date_received=log_date).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
                diesel_received_info.fuel_name = diesel_received_info.fuel.fuel_type
                diesel_received_info.save()
                diesel_received_info.refresh_from_db()
            fuel_received_info = FuelReceived.objects.all().filter(fuel_id=diesel_id).filter(date_received=log_date)
        serializers = FuelReceivedSerializer(fuel_received_info,many=True)
        return Response(serializers.data)

class GasReceivedTodayInfo(APIView):
    permission_classes=(AllowAny,)
    def get_fuel_received_info(self,id):
        gas_info = Fuel.objects.all().filter(fuel_type='Gas').last()
        if gas_info:
            print(gas_info)
            print(gas_info.id)
            gas_id = gas_info.id
        else:
            Http404
        log_details = Log.objects.all().filter(id=id).filter(fuel_id=gas_id).first() 
        if log_details:
            log_date = log_details.date
            try:
                return FuelReceived.objects.all().filter(fuel_id=gas_id).filter(date_received=log_date)
            except FuelReceived.DoesNotExist:
                return Http404
        else:
            Http404
    
    def get(self, request, id, format=None):
        today = dt.date.today()
        gas_info = Fuel.objects.all().filter(fuel_type='Gas').last()
        if gas_info:
            print(gas_info)
            print(gas_info.id)
            gas_id = gas_info.id
        else:
            Http404
        log_details = Log.objects.all().filter(id=id).filter(fuel_id=gas_id).first() 
        if log_details:
            log_date = log_details.date
            gas_received_info = FuelReceived.objects.all().filter(fuel_id=gas_id).last()
            if gas_received_info:
                gas_received_info.total_fuel_received_today = FuelReceived.objects.all().filter(fuel_id=gas_id).filter(date_received=log_date).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
                gas_received_info.fuel_name = gas_received_info.fuel.fuel_type
                gas_received_info.save()
                gas_received_info.refresh_from_db()
            fuel_received_info = FuelReceived.objects.all().filter(fuel_id=gas_id).filter(date_received=log_date)
        serializers = FuelReceivedSerializer(fuel_received_info,many=True)
        return Response(serializers.data)
        

class LogDetails(APIView):
    permission_classes=(AllowAny,)
    def get_log_details(self,id):
        try:
            return Log.objects.all().filter(pk=id).first()
        except Log.DoesNotExist:
            return Http404
    
    def get(self, request, id, format=None):
        log_details = Log.objects.all().filter(pk=id).first()
        serializers = LogSerializer(log_details,many=False)
        return Response(serializers.data)

    def put(self, request, id, format=None):
        log_details = Log.objects.all().filter(pk=id).first()
        serializers = LogSerializer(log_details,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class MpesaLogDetails(APIView):
    permission_classes=(AllowAny,)
    def get_mpesa_details(self,id):
        try:
            return LogMpesa.objects.all().filter(id=id).last()
        except LogMpesa.DoesNotExist:
            return Http404
    
    def get(self, request, id, format=None):
        mpesa_details = LogMpesa.objects.all().filter(id=id).last()
        if mpesa_details:
            mpesa_date = mpesa_details.date
        mpesa_today = LogMpesa.objects.all().filter(date=mpesa_date)
        if mpesa_details and mpesa_today:
            mpesa_details.daily_total = LogMpesa.objects.all().filter(date=mpesa_date).aggregate(TOTAL = Sum('amount'))['TOTAL']
            mpesa_details.save()
            mpesa_details.cumulative_amount = LogMpesa.objects.all().aggregate(TOTAL = Sum('amount'))['TOTAL']
            mpesa_details.save()
            mpesa_details.refresh_from_db()
        elif mpesa_details:
            mpesa_details.daily_total = 0
            mpesa_details.save()
            mpesa_details.cumulative_amount = LogMpesa.objects.all().aggregate(TOTAL = Sum('amount'))['TOTAL']
            mpesa_details.save()
            mpesa_details.refresh_from_db()
        serializers = LogMpesaSerializer(mpesa_details,many=False)
        return Response(serializers.data)

    def put(self, request, id, format=None):
        mpesa_details = LogMpesa.objects.all().filter(id=id).first()
        serializers = LogMpesaSerializer(mpesa_details,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class PastLogs(APIView):
    permission_classes=(AllowAny,)
    def get_past_logs(self,past_date):
        try:
            date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()
        except ValueError:
            raise Http404()
            assert False 
    
    def get(self,past_date):
        past_logs = Log.objects.all().filter(date=past_date)
        serializers = LogSerializer(past_logs,many=True)
        return Response(serializers.data)

class EmailReport(APIView):
    permission_classes=(AllowAny,)
    def get_reports(self):
        try:
            return LogReport.objects.all()
        except LogReport.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        reports = LogReport.objects.all()
        serializers = LogSerializer(reports,many=True)
        return Response(serializers.data)

    def post(self, request,format=None):
        serializers = LogReportSerializer(data=request.data)
        if serializers.is_valid():
            # serializer.is_valid(raise_exception=True)
            eod_reading_lts=serializers.validated_data['eod_reading_lts']
            eod_reading_yesterday=serializers.validated_data['eod_reading_yesterday']
            litres_sold_today=serializers.validated_data['litres_sold_today']
            amount_earned_today=serializers.validated_data['amount_earned_today']
            balance=serializers.validated_data['balance']
            username=serializers.validated_data['admin_name']
            receiver=serializers.validated_data['admin_email']
            serializers.save()
            
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = "Here is your requested email report:</p> <br> <ul><li>eod: " + str(eod_reading_lts) + " </li>eod_yesterday: " + str(eod_reading_yesterday) + " <li>litres sold: " + str(litres_sold_today) + " </li>amount: " + str(amount_earned_today) + " <li>bal: " + str(balance) + "</li></ul> <br> <small> The data committee, <br> LogOnGo. <br> ©Pebo Kenya Ltd  </small>"
            message = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = receiver,
                subject = "Your email report",
                html_content='<p>Hello, ' + str(username) + '! <br><br>' + msg
            )
            try:
                sendgrid_client = sendgrid.SendGridAPIClient(config('SENDGRID_API_KEY'))
                response = sendgrid_client.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)
            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'True',
                'status code' : status_code,
                'message': 'Email report sent  successfully',
                }
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EmailMpesaReport(APIView):
    permission_classes=(AllowAny,)
    def get_mpesa_reports(self):
        try:
            return MpesaReport.objects.all()
        except MpesaReport.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        reports = MpesaReport.objects.all()
        serializers = MpesaReportSerializer(reports,many=True)
        return Response(serializers.data)

    def post(self, request,format=None):
        serializers = MpesaReportSerializer(data=request.data)
        if serializers.is_valid():
            # serializer.is_valid(raise_exception=True)
            date=serializers.validated_data['date']
            transaction_number=serializers.validated_data['transaction_number']
            customer_name=serializers.validated_data['customer_name']
            customer_phone_number=serializers.validated_data['customer_phone_number']
            amount=serializers.validated_data['amount']
            amount_transferred_to_bank=serializers.validated_data['amount_transferred_to_bank']
            daily_total=serializers.validated_data['daily_total']
            cumulative_amount=serializers.validated_data['cumulative_amount']
            logged_by=serializers.validated_data['logged_by']
            username=serializers.validated_data['admin_name']
            receiver=serializers.validated_data['admin_email']
            serializers.save()
            
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = "Here is your requested email report:</p> <br> <ul><li>date: " + str(date) + " </li><li>transaction no.: " + str(transaction_number) + "</li><li>customer's name: " + str(customer_name) + " </li><li>customer's phone number: " + str(customer_phone_number) + "</li><li>amount: " + str(amount) + "</li><li>amount transferred to bank: " + str(amount_transferred_to_bank) + "</li><li>daily total: " + str(daily_total) + "</li><li>cumulative amount: " + str(cumulative_amount) + "</li><li>logged by: " + str(logged_by) + "</li></ul> <br> <small> The data committee, <br> LogOnGo. <br> ©Pebo Kenya Ltd  </small>"
            message = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = receiver,
                subject = "Your Mpesa report",
                html_content='<p>Hello, ' + str(username) + '! <br><br>' + msg
            )
            try:
                sendgrid_client = sendgrid.SendGridAPIClient(config('SENDGRID_API_KEY'))
                response = sendgrid_client.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)
            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'True',
                'status code' : status_code,
                'message': 'Email report sent  successfully',
                }
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class IncidentReport(APIView):
    permission_classes=(AllowAny,)
    def get_incident_reports(self):
        try:
            return Incident.objects.all()
        except IncidentReport.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        reports = Incident.objects.all()
        serializers = IncidentSerializer(reports,many=True)
        return Response(serializers.data)

    def post(self, request,format=None):
        serializers = IncidentSerializer(data=request.data)
        if serializers.is_valid():
            # serializer.is_valid(raise_exception=True)
            nature=serializers.validated_data['nature']
            description=serializers.validated_data['description']
            username=serializers.validated_data['your_name']
            incident_date=serializers.validated_data['incident_date']
            # date_and_time_reported=serializers.validated_data['date_and_time_reported']
            sender=serializers.validated_data['your_email']
            receiver='fullstack.benie@gmail.com'
            admin='Janja'
            serializers.save()
            
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = "An incident has been reported on LogOnGo. Here are the details::</p> <br> <ul><li>nature: " + str(nature) + " </li><li>description: " + str(description) + "</li><li>reported by: " + str(username) + " </li><li>report email: " + str(sender) + "</li><li>incident date: " + str(incident_date) + "</li></ul> <br> <small> The contact team, <br> LogOnGo. <br> ©Pebo Kenya Ltd  </small>"
            message = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = receiver,
                subject = "Incident Report",
                html_content='<p>Hello, ' + str(admin) + '! <br><br>' + msg
            )
            try:
                sendgrid_client = sendgrid.SendGridAPIClient(config('SENDGRID_API_KEY'))
                response = sendgrid_client.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)
            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'True',
                'status code' : status_code,
                'message': 'Email report sent  successfully',
                }
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ContactAdmin(APIView):
    permission_classes=(AllowAny,)
    def get_incident_reports(self):
        try:
            return Contact.objects.all()
        except Contact.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        reports = Contact.objects.all()
        serializers = ContactSerializer(reports,many=True)
        return Response(serializers.data)

    def post(self, request,format=None):
        serializers = ContactSerializer(data=request.data)
        if serializers.is_valid():
            # serializer.is_valid(raise_exception=True)
            contact_subject=serializers.validated_data['subject']
            contact_message=serializers.validated_data['message']
            your_name=serializers.validated_data['your_name']
            sender=serializers.validated_data['your_email']
            # date_and_time_reported=serializers.validated_data['date_and_time_reported']
            receiver='fullstack.benie@gmail.com'
            admin='Janja'
            serializers.save()
            
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = "You have received a message on LogOnGo from " + str(your_name) + " of the email: " + str(sender) + ". Here is the message::</p> <br> <p>" + str(contact_message) + "</p> <br> <small> The contact team, <br> LogOnGo. <br> ©Pebo Kenya Ltd  </small>"
            message = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = receiver,
                subject = contact_subject,
                html_content='<p>Hello, ' + str(admin) + '! <br><br>' + msg
            )
            try:
                sendgrid_client = sendgrid.SendGridAPIClient(config('SENDGRID_API_KEY'))
                response = sendgrid_client.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)
            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'True',
                'status code' : status_code,
                'message': 'Email report sent  successfully',
                }
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    