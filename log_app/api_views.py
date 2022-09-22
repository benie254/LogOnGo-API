import sendgrid
from sendgrid.helpers.mail import * 
import os 
from decouple import config 
from django.shortcuts import get_object_or_404, render,redirect 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from log_app.serializer import FuelReceivedSerializer, FuelSerializer, LogMpesaSerializer, LogReportSerializer, LogSerializer, AnnouncementSerializer,LogReport


from django.http import HttpResponse,Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from log_app.models import Fuel, FuelReceived, LogReport, MpesaReport, MyUser 
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

class TodayFuelLogs(APIView):
    permission_classes=(AllowAny,)
    def get_today_fuel_logs(self,id):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=id).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, id, format=None):
        c_user_id = request.user.id
        today = dt.date.today()
        today_fuel_log = Log.objects.all().filter(date=today).filter(fuel_id=id).first()
        petrol_received_info = FuelReceived.objects.all().filter(fuel_id=id).last()
        petrol_received = FuelReceived.objects.all().filter(fuel_id=id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        yesterday = today - dt.timedelta(days=1)
        yesterday_petrol_logs = Log.objects.all().filter(date=yesterday).first()
        petrol_info = Fuel.objects.all().filter(fuel_type='Petrol').last()
        if today_fuel_log and petrol_info:
            petrol_pp = petrol_info.price_per_litre 
            today_fuel_log.fuel_name = today_fuel_log.fuel.fuel_type
            today_fuel_log.save()
            today_fuel_log.total_litres_sold = ExpressionWrapper(F('eod_reading_lts')-F('eod_reading_yesterday'),output_field=DecimalField())
            today_fuel_log.save()
            total_sold = today_fuel_log.total_litres_sold
            today_fuel_log.amount_earned_today = ExpressionWrapper(F('total_litres_sold') * (petrol_pp),output_field=PositiveIntegerField())
            today_fuel_log.save()
            today_fuel_log.refresh_from_db()
            today_fuel_log.logged_by = request.user.username 
            today_fuel_log.save()
            # user_id = MyUser.objects.get(id=c_user_id)
            # today_fuel_log.user_id = user_id
            # today_fuel_log.save()
            # today_fuel_log.refresh_from_db()
            if yesterday_petrol_logs:
                eod_yesterday = yesterday_petrol_logs.eod_reading_lts
                today_fuel_log.eod_reading_yesterday = eod_yesterday
                today_fuel_log.save()
                bal_yesterday = yesterday_petrol_logs.balance
                today_fuel_log.balance_yesterday = bal_yesterday
                today_fuel_log.save()
                yesterday_bal = today_fuel_log.balance_yesterday
                today_fuel_log.balance = F('balance_yesterday') - F('total_litres_sold')
                today_fuel_log.save()
                today_fuel_log.refresh_from_db()
                bal = today_fuel_log.balance 
            else:
                init = petrol_info.initial_litres_in_tank
                today_fuel_log.balance = (init) - F('total_litres_sold')
                bal = today_fuel_log.balance 
            if bal and petrol_received:
                petrol_amount = petrol_received
                today_fuel_log.updated_balance = F('balance')+ (petrol_received)
                today_fuel_log.save()
                today_fuel_log.refresh_from_db()              
            elif today_fuel_log.updated_balance and petrol_received:
                petrol_amount = petrol_received
                today_fuel_log.updated_balance = F('updated_balance')+ (petrol_amount)
                today_fuel_log.save(update_fields=['updated_balance'])
                today_fuel_log.refresh_from_db() 
        serializers = LogSerializer(today_fuel_log,many=False)
        return Response(serializers.data)

class TodayFuelLogsTwo(APIView):
    permission_classes=(AllowAny,)
    def get_today_fuel_logs_two(self,id):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=id).order_by('-date')[:2]
        except Log.DoesNotExist:
            return Http404

    def get(self, request, id, format=None):
        today = dt.date.today()
        today_fuel_logs_two = Log.objects.all().filter(date=today).filter(fuel_id=id).order_by('-date')[:2]
        serializers = LogSerializer(today_fuel_logs_two,many=True)
        return Response(serializers.data)

class TodayFuelLogsThree(APIView):
    permission_classes=(AllowAny,)
    def get_today_fuel_logs_three(self,id):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=id).order_by('-date')[:3]
        except Log.DoesNotExist:
            return Http404

    def get(self, request, id, format=None):
        today = dt.date.today()
        today_fuel_logs_three = Log.objects.all().filter(date=today).filter(fuel_id=id).order_by('-date')[:3]
        serializers = LogSerializer(today_fuel_logs_three,many=True)
        return Response(serializers.data)

class TodayFuelLogsFour(APIView):
    permission_classes=(AllowAny,)
    def get_today_fuel_logs_four(self, id):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=id).order_by('-date')[:4]
        except Log.DoesNotExist:
            return Http404

    def get(self, request, id, format=None):
        today = dt.date.today()
        today_fuel_logs_four = Log.objects.all().filter(date=today).filter(fuel_id=id).order_by('-date')[:4]
        serializers = LogSerializer(today_fuel_logs_four,many=True)
        return Response(serializers.data)

class YesterdayFuelLogs(APIView):
    permission_classes=(AllowAny,)
    def get_yesterday_fuel_logs(self,id):
        today = dt.date.today()
        yesterday = today - dt.timedelta(days=1)
        try:
            return Log.objects.all().filter(date=yesterday).filter(fuel_id=id).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, id, format=None):
        today = dt.date.today()
        yesterday = today - dt.timedelta(days=1)
        yesterday_fuel_logs = Log.objects.all().filter(date=yesterday).filter(fuel_id=id).first()
        serializers = LogSerializer(yesterday_fuel_logs,many=False)
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

class MpesaCumulative(APIView):
    permission_classes=(AllowAny,)
    def get_mpesa_total(self):
        try:
            return LogMpesa.objects.all().aggregate(TOTAL = Sum('amount'))['TOTAL']
        except LogMpesa.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        mpesa_total = LogMpesa.objects.all().aggregate(TOTAL = Sum('amount'))['TOTAL']
        serializers = LogMpesaSerializer(mpesa_total,many=False)
        return Response(serializers.data)

class MpesaTodayTotal(APIView):
    permission_classes=(AllowAny,)
    def get_mpesa_total(self):
        today = dt.date.today()
        try:
            return LogMpesa.objects.all().filter(date=today).aggregate(TOTAL = Sum('amount'))['TOTAL']
        except LogMpesa.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        mpesa_total = LogMpesa.objects.all().filter(date=today).aggregate(TOTAL = Sum('amount'))['TOTAL']
        serializers = LogMpesaSerializer(mpesa_total,many=False)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = LogMpesaSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class TotalPetrolReceivedToday(APIView):
    permission_classes=(AllowAny,)
    def get_fuel_received(self):
        today = dt.date.today()
        petrol_info = Fuel.objects.all().filter(fuel_type='Petrol').last()
        print(petrol_info)
        petrol_id = petrol_info.id
        try:
            return FuelReceived.objects.all().filter(fuel_id=petrol_id).filter(date_received=today).last()
        except FuelReceived.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        petrol_info = Fuel.objects.all().filter(fuel_type='Petrol').last()
        print(petrol_info)
        print(petrol_info.id)
        petrol_id = petrol_info.id
        fuel_received = FuelReceived.objects.all().filter(fuel_id=petrol_id).filter(date_received=today).last()
        if fuel_received:
            fuel_received.total_fuel_received_today = FuelReceived.objects.all().filter(fuel_id=petrol_id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
            fuel_received.fuel_name = fuel_received.fuel.fuel_type
            fuel_received.save()
            fuel_received.refresh_from_db()
        serializers = FuelReceivedSerializer(fuel_received,many=False)
        return Response(serializers.data)

class TotalDieselReceivedToday(APIView):
    permission_classes=(AllowAny,)
    def get_fuel_received(self):
        today = dt.date.today()
        petrol_info = Fuel.objects.all().filter(fuel_type='Diesel').last()
        print(petrol_info)
        petrol_id = petrol_info.id
        try:
            return FuelReceived.objects.all().filter(fuel_id=petrol_id).filter(date_received=today).last()
        except FuelReceived.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        petrol_info = Fuel.objects.all().filter(fuel_type='Diesel').last()
        print(petrol_info)
        print(petrol_info.id)
        petrol_id = petrol_info.id
        fuel_received = FuelReceived.objects.all().filter(fuel_id=petrol_id).filter(date_received=today).last()
        if fuel_received:
            fuel_received.total_fuel_received_today = FuelReceived.objects.all().filter(fuel_id=petrol_id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
            fuel_received.fuel_name = fuel_received.fuel.fuel_type
            fuel_received.save()
            fuel_received.refresh_from_db()
        serializers = FuelReceivedSerializer(fuel_received,many=False)
        return Response(serializers.data)

class TotalGasReceivedToday(APIView):
    permission_classes=(AllowAny,)
    def get_fuel_received(self):
        today = dt.date.today()
        petrol_info = Fuel.objects.all().filter(fuel_type='Gas').last()
        print(petrol_info)
        petrol_id = petrol_info.id
        try:
            return FuelReceived.objects.all().filter(fuel_id=petrol_id).filter(date_received=today).last()
        except FuelReceived.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        petrol_info = Fuel.objects.all().filter(fuel_type='Gas').last()
        print(petrol_info)
        print(petrol_info.id)
        petrol_id = petrol_info.id
        fuel_received = FuelReceived.objects.all().filter(fuel_id=petrol_id).filter(date_received=today).last()
        if fuel_received:
            fuel_received.total_fuel_received_today = FuelReceived.objects.all().filter(fuel_id=petrol_id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
            fuel_received.fuel_name = fuel_received.fuel.fuel_type
            fuel_received.save()
            fuel_received.refresh_from_db()
        serializers = FuelReceivedSerializer(fuel_received,many=False)
        return Response(serializers.data)

class FuelReceivedToday(APIView):
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


class FuelReceivedTodayInfo(APIView):
    permission_classes=(AllowAny,)
    def get_fuel_received_info(self,id):
        today = dt.date.today()
        try:
            return FuelReceived.objects.all().filter(fuel_id=id).filter(date_received=today)
        except FuelReceived.DoesNotExist:
            return Http404
    
    def get(self, request, id, format=None):
        today = dt.date.today()
        petrol_received_info = FuelReceived.objects.all().filter(fuel_id=id).last()
        if petrol_received_info:
            petrol_received_info.total_fuel_received_today = FuelReceived.objects.all().filter(fuel_id=id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
            petrol_received_info.fuel_name = petrol_received_info.fuel.fuel_type
            petrol_received_info.save()
            petrol_received_info.refresh_from_db()
        fuel_received_info = FuelReceived.objects.all().filter(fuel_id=id).filter(date_received=today)
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
        today = dt.date.today()
        petrol_info = Fuel.objects.all().filter(fuel_type='Petrol').last()
        log_details.total_litres_sold = ExpressionWrapper(F('eod_reading_yesterday')-F('eod_reading_lts'),output_field=DecimalField())
        log_details.save()
        log_details.refresh_from_db()
        total_sold = log_details.total_litres_sold
        petrol_received = FuelReceived.objects.all().filter(fuel_id=1).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        yesterday = today - dt.timedelta(days=1)
        yesterday_petrol_logs = Log.objects.all().filter(date=yesterday).first()
        if log_details and petrol_info:
            petrol_pp = petrol_info.price_per_litre 
            log_details.fuel_name = log_details.fuel.fuel_type
            log_details.save()
            log_details.total_litres_sold = ExpressionWrapper(F('eod_reading_lts')-F('eod_reading_yesterday'),output_field=DecimalField())
            log_details.save()
            total_sold = log_details.total_litres_sold
            log_details.amount_earned_today = ExpressionWrapper(F('total_litres_sold') * (petrol_pp),output_field=PositiveIntegerField())
            log_details.save()
            log_details.refresh_from_db()
            log_details.logged_by = request.user.username 
            log_details.save()
            # user_id = MyUser.objects.get(id=c_user_id)
            # log_details.user_id = user_id
            # log_details.save()
            # log_details.refresh_from_db()
            if yesterday_petrol_logs:
                eod_yesterday = yesterday_petrol_logs.eod_reading_lts
                log_details.eod_reading_yesterday = eod_yesterday
                log_details.save()
                bal_yesterday = yesterday_petrol_logs.balance
                log_details.balance_yesterday = bal_yesterday
                log_details.save()
                yesterday_bal = log_details.balance_yesterday
                log_details.balance = F('balance_yesterday') - F('total_litres_sold')
                log_details.save()
                log_details.refresh_from_db()
                bal = log_details.balance 
            else:
                init = petrol_info.initial_litres_in_tank
                log_details.balance = (init) - F('total_litres_sold')
                bal = log_details.balance 
            if bal and petrol_received:
                petrol_amount = petrol_received
                log_details.updated_balance = F('balance')+ (petrol_received)
                log_details.save()
                log_details.refresh_from_db()              
            elif log_details.updated_balance and petrol_received:
                petrol_amount = petrol_received
                log_details.updated_balance = F('updated_balance')+ (petrol_amount)
                log_details.save(update_fields=['updated_balance'])
                log_details.refresh_from_db() 
        
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
            return LogMpesa.objects.all().filter(pk=id)
        except LogMpesa.DoesNotExist:
            return Http404
    
    def get(self, request, id, format=None):
        mpesa_details = LogMpesa.objects.all().filter(pk=id)
        serializers = LogMpesaSerializer(mpesa_details,many=False)
        return Response(serializers.data)

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
    