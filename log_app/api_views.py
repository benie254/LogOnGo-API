import None
from django.shortcuts import get_object_or_404, render,redirect 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from log_app.serializer import FuelReceivedSerializer, FuelSerializer, LogMpesaSerializer, LogSerializer, MyUserSerializer

from django.http import HttpResponse,Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from log_app.models import Fuel, FuelReceived, LogReport, MpesaReport, MyUser 
import datetime as dt 
from django.db.models import Sum
from django.contrib import messages

from log_app.models import Announcement, Contact, Incident, Log, LogMpesa

# Create your views here.
class ProfileDetails(APIView):
    def get_profile_details(self, id):
        try:
            return MyUser.objects.all().filter(pk=id) 
        except MyUser.DoesNotExist:
            return Http404
    
    def get(self, request, id, format=None):
        profile_details = MyUser.objects.all().filter(pk=id)
        serializers = MyUserSerializer(profile_details,many=False)
        return Response(serializers.data)

class RegisteredFuels(APIView):
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
    def get_today_fuel_logs(self,id):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=id).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, id, format=None):
        today = dt.date.today()
        today_fuel_logs = Log.objects.all().filter(date=today).filter(fuel_id=id).first()
        serializers = LogSerializer(today_fuel_logs,many=False)
        return Response(serializers.data)

class TodayFuelLogsTwo(APIView):
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
    def get_user_mpesa_logs(self,id):
        try:
            return LogMpesa.objects.all().filter(user_id=id).order_by('-date')
        except LogMpesa.DoesNotExist:
            return Http404

    def get(self, request, id, format=None):
        user_mpesa_logs = LogMpesa.objects.all().filter(user_id=id).order_by('-date')
        serializers = LogMpesaSerializer(user_mpesa_logs,many=True)
        return Response(serializers.data)

class MpesaCumulative(APIView):
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

class TotalFuelReceivedToday(APIView):
    def get_fuel_received(self,id):
        today = dt.date.today()
        try:
            return FuelReceived.objects.all().filter(fuel_id=id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        except FuelReceived.DoesNotExist:
            return Http404
    
    def get(self, request, id, format=None):
        today = dt.date.today()
        fuel_received = FuelReceived.objects.all().filter(fuel_id=id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        serializers = FuelReceivedSerializer(fuel_received,many=False)
        return Response(serializers.data)

class FuelReceivedTodayInfo(APIView):
    def get_fuel_received_info(self,id):
        today = dt.date.today()
        try:
            return FuelReceived.objects.all().filter(fuel_id=id).filter(date_received=today)
        except FuelReceived.DoesNotExist:
            return Http404
    
    def get(self, request, id, format=None):
        today = dt.date.today()
        fuel_received_info = FuelReceived.objects.all().filter(fuel_id=id).filter(date_received=today)
        serializers = FuelReceivedSerializer(fuel_received_info,many=True)
        return Response(serializers.data)

class LogDetails(APIView):
    def get_log_details(self,id):
        try:
            return Log.objects.all().filter(pk=id).first()
        except Log.DoesNotExist:
            return Http404
    
    def get(self, request, id, format=None):
        log_details = Log.objects.all().filter(pk=id).first()
        serializers = LogSerializer(log_details,many=False)
        return Response(serializers.data)

class MpesaLogDetails(APIView):
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