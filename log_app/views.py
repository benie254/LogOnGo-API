from django.shortcuts import get_object_or_404, render,redirect 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from log_app.serializer import FuelReceivedSerializer, FuelSerializer, LogMpesaSerializer, LogSerializer, MyUserSerializer, PetrolInfoSerializer

from django.http import HttpResponse,Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from log_app.models import Fuel, FuelReceived, LogReport, MpesaReport, MyUser 
import datetime as dt 
from django.db.models import Sum
from django.contrib import messages

from log_app.models import Announcement, Contact, Incident, Log, LogMpesa

# Create your views here.
class ProfileDetails(APIView):
    def get_profile_details(self, user_id):
        try:
            return MyUser.objects.all().filter(pk=user_id) 
        except MyUser.DoesNotExist:
            return Http404
    
    def get(self, request, user_id, format=None):
        profile_details = MyUser.objects.all().filter(pk=user_id)
        serializers = MyUserSerializer(profile_details,many=False)
        return Response(serializers.data)

class RegisteredFuels(APIView):
    def post(self, request, format=None):
        serializers = FuelSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

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
    def get_gas_info(self,fuel_id):
        try:
            return Fuel.objects.all().filter(id=3).last()
        except Fuel.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        gas_info = Fuel.objects.all().filter(id=3).last()
        serializers = FuelSerializer(gas_info,many=False)
        return Response(serializers.data)

class DieselInfo(APIView):
    def get_diesel_info(self,fuel_id):
        try:
            return Fuel.objects.all().filter(id=1).last()
        except Fuel.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        diesel_info = Fuel.objects.all().filter(id=1).last()
        serializers = FuelSerializer(diesel_info,many=False)
        return Response(serializers.data)

class PetrolInfo(APIView):
    def get_petrol_info(self,fuel_id):
        try:
            return Fuel.objects.all().filter(id=2).last()
        except Fuel.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        petrol_info = Fuel.objects.all().filter(id=2).last()
        serializers = FuelSerializer(petrol_info,many=False)
        return Response(serializers.data)

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

class UserLogs(APIView):
    def get_user_logs(self,user_id):
        try:
            return Log.objects.all().filter(user_id=user_id).order_by('-date')
        except Log.DoesNotExist:
            return Http404

    def get(self, request, user_id, format=None):
        user_logs = Log.objects.all().filter(user_id=user_id).order_by('-date')
        serializers = LogSerializer(user_logs,many=True)
        return Response(serializers.data)

class TodayDieselLogs(APIView):
    def get_today_diesel_logs(self):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=1).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        today_diesel_logs = Log.objects.all().filter(date=today).filter(fuel_id=1).first()
        serializers = LogSerializer(today_diesel_logs,many=False)
        return Response(serializers.data)

class TodayDieselLogsTwo(APIView):
    def get_today_diesel_logs_two(self):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=1).order_by('-date')[:2]
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        today_diesel_logs_two = Log.objects.all().filter(date=today).filter(fuel_id=1).order_by('-date')[:2]
        serializers = LogSerializer(today_diesel_logs_two,many=True)
        return Response(serializers.data)

class TodayDieselLogsThree(APIView):
    def get_today_diesel_logs_three(self):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=1).order_by('-date')[:3]
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        today_diesel_logs_three = Log.objects.all().filter(date=today).filter(fuel_id=1).order_by('-date')[:3]
        serializers = LogSerializer(today_diesel_logs_three,many=True)
        return Response(serializers.data)

class TodayDieselLogsFour(APIView):
    def get_today_diesel_logs_four(self):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=1).order_by('-date')[:4]
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        today_diesel_logs_four = Log.objects.all().filter(date=today).filter(fuel_id=1).order_by('-date')[:4]
        serializers = LogSerializer(today_diesel_logs_four,many=True)
        return Response(serializers.data)

class TodayPetrolLogs(APIView):
    def get_today_petrol_logs(self):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=2).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        today_petrol_logs = Log.objects.all().filter(date=today).filter(fuel_id=2).first()
        serializers = LogSerializer(today_petrol_logs,many=False)
        return Response(serializers.data)

class TodayPetrolLogsTwo(APIView):
    def get_today_petrol_logs_two(self):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=2).order_by('-date')[:2]
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        today_petrol_logs_two = Log.objects.all().filter(date=today).filter(fuel_id=2).order_by('-date')[:2]
        serializers = LogSerializer(today_petrol_logs_two,many=True)
        return Response(serializers.data)

class TodayPetrolLogsThree(APIView):
    def get_today_petrol_logs_three(self):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=2).order_by('-date')[:3]
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        today_petrol_logs_three = Log.objects.all().filter(date=today).filter(fuel_id=2).order_by('-date')[:3]
        serializers = LogSerializer(today_petrol_logs_three,many=True)
        return Response(serializers.data)

class TodayPetrolLogsFour(APIView):
    def get_today_petrol_logs_four(self):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=2).order_by('-date')[:4]
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        today_petrol_logs_four = Log.objects.all().filter(date=today).filter(fuel_id=2).order_by('-date')[:4]
        serializers = LogSerializer(today_petrol_logs_four,many=True)
        return Response(serializers.data)

class TodayGasLogs(APIView):
    def get_today_gas_logs(self):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=3).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        today_gas_logs = Log.objects.all().filter(date=today).filter(fuel_id=3).first()
        serializers = LogSerializer(today_gas_logs,many=False)
        return Response(serializers.data)

class TodayGasLogsTwo(APIView):
    def get_today_gas_logs_two(self):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=3).order_by('-date')[:3]
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        today_gas_logs_two = Log.objects.all().filter(date=today).filter(fuel_id=3).order_by('-date')[:3]
        serializers = LogSerializer(today_gas_logs_two,many=True)
        return Response(serializers.data)

class TodayGasLogsThree(APIView):
    def get_today_gas_logs_three(self):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=3).order_by('-date')[:3]
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        today_gas_logs_three = Log.objects.all().filter(date=today).filter(fuel_id=3).order_by('-date')[:3]
        serializers = LogSerializer(today_gas_logs_three,many=True)
        return Response(serializers.data)

class TodayGasLogsFour(APIView):
    def get_today_gas_logs_four(self):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=3).order_by('-date')[:4]
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        today_gas_logs_four = Log.objects.all().filter(date=today).filter(fuel_id=3).order_by('-date')[:4]
        serializers = LogSerializer(today_gas_logs_four,many=True)
        return Response(serializers.data)

class YesterdayDieselLogs(APIView):
    def get_yesterday_diesel_logs(self):
        yesterday = yesterday - dt.timedelta(days=1)
        try:
            return Log.objects.all().filter(date=yesterday).filter(fuel_id=1).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        yesterday = yesterday - dt.timedelta(days=1)
        yesterday_diesel_logs = Log.objects.all().filter(date=yesterday).filter(fuel_id=1).first()
        serializers = LogSerializer(yesterday_diesel_logs,many=False)
        return Response(serializers.data)

class YesterdayPetrolLogs(APIView):
    def get_yesterday_petrol_logs(self):
        yesterday = yesterday - dt.timedelta(days=1)
        try:
            return Log.objects.all().filter(date=yesterday).filter(fuel_id=2).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        yesterday = yesterday - dt.timedelta(days=1)
        yesterday_petrol_logs = Log.objects.all().filter(date=yesterday).filter(fuel_id=2).first()
        serializers = LogSerializer(yesterday_petrol_logs,many=False)
        return Response(serializers.data)

class YesterdayGasLogs(APIView):
    def get_yesterday_gas_logs(self):
        yesterday = yesterday - dt.timedelta(days=1)
        try:
            return Log.objects.all().filter(date=yesterday).filter(fuel_id=3).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        yesterday = yesterday - dt.timedelta(days=1)
        yesterday_gas_logs = Log.objects.all().filter(date=yesterday).filter(fuel_id=3).first()
        serializers = LogSerializer(yesterday_gas_logs,many=False)
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

class UserMpesaLogs(APIView):
    def get_user_mpesa_logs(self,user_id):
        try:
            return LogMpesa.objects.all().filter(user_id=user_id).order_by('-date')
        except LogMpesa.DoesNotExist:
            return Http404

    def get(self, request, user_id, format=None):
        user_mpesa_logs = LogMpesa.objects.all().filter(user_id=user_id).order_by('-date')
        serializers = LogMpesaSerializer(user_mpesa_logs,many=True)
        return Response(serializers.data)

class MpesaTotal(APIView):
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

class TotalDieselReceivedToday(APIView):
    def get_diesel_received(self):
        today = dt.date.today()
        try:
            return FuelReceived.objects.all().filter(fuel_id=1).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        except FuelReceived.DoesNotExist:
            return Http404
    
    def get(self, request, format=None):
        today = dt.date.today()
        diesel_received = FuelReceived.objects.all().filter(fuel_id=1).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        serializers = FuelReceivedSerializer(diesel_received,many=False)
        return Response(serializers.data)

class DieselReceivedTodayInfo(APIView):
    def get_diesel_received_info(self):
        today = dt.date.today()
        try:
            return FuelReceived.objects.all().filter(fuel_id=1).filter(date_received=today)
        except FuelReceived.DoesNotExist:
            return Http404
    
    def get(self, request, format=None):
        today = dt.date.today()
        diesel_received_info = FuelReceived.objects.all().filter(fuel_id=1).filter(date_received=today)
        serializers = FuelReceivedSerializer(diesel_received_info,many=True)
        return Response(serializers.data)

class TotalPetrolReceivedToday(APIView):
    def get_petrol_received(self):
        today = dt.date.today()
        try:
            return FuelReceived.objects.all().filter(fuel_id=2).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        except FuelReceived.DoesNotExist:
            return Http404
    
    def get(self, request, format=None):
        today = dt.date.today()
        petrol_received = FuelReceived.objects.all().filter(fuel_id=2).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        serializers = FuelReceivedSerializer(petrol_received,many=False)
        return Response(serializers.data)

class PetrolReceivedTodayInfo(APIView):
    def get_petrol_received_info(self):
        today = dt.date.today()
        try:
            return FuelReceived.objects.all().filter(fuel_id=2).filter(date_received=today)
        except FuelReceived.DoesNotExist:
            return Http404
    
    def get(self, request, format=None):
        today = dt.date.today()
        petrol_received_info = FuelReceived.objects.all().filter(fuel_id=2).filter(date_received=today)
        serializers = FuelReceivedSerializer(petrol_received_info,many=True)
        return Response(serializers.data)

class TotalGasReceivedToday(APIView):
    def get_gas_received(self):
        today = dt.date.today()
        try:
            return FuelReceived.objects.all().filter(fuel_id=3).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        except FuelReceived.DoesNotExist:
            return Http404
    
    def get(self, request, format=None):
        today = dt.date.today()
        gas_received = FuelReceived.objects.all().filter(fuel_id=3).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        serializers = FuelReceivedSerializer(gas_received,many=False)
        return Response(serializers.data)

class GasReceivedTodayInfo(APIView):
    def get_gas_received_info(self):
        today = dt.date.today()
        try:
            return FuelReceived.objects.all().filter(fuel_id=3).filter(date_received=today)
        except FuelReceived.DoesNotExist:
            return Http404
    
    def get(self, request, format=None):
        today = dt.date.today()
        gas_received_info = FuelReceived.objects.all().filter(fuel_id=3).filter(date_received=today)
        serializers = FuelReceivedSerializer(gas_received_info,many=True)
        return Response(serializers.data)

class DieselLogDetails(APIView):
    def get_diesel_details(self,log_id):
        try:
            return Log.objects.all().filter(fuel_id=1).filter(pk=log_id).first()
        except Log.DoesNotExist:
            return Http404
    
    def get(self, request, log_id, format=None):
        today = dt.date.today()
        diesel_details = Log.objects.all().filter(fuel_id=1).filter(pk=log_id).first()
        serializers = LogSerializer(diesel_details,many=False)
        return Response(serializers.data)

class PetrolLogDetails(APIView):
    def get_petrol_details(self,log_id):
        try:
            return Log.objects.all().filter(fuel_id=2).filter(pk=log_id).first()
        except Log.DoesNotExist:
            return Http404
    
    def get(self, request, log_id, format=None):
        today = dt.date.today()
        petrol_details = Log.objects.all().filter(fuel_id=2).filter(pk=log_id).first()
        serializers = LogSerializer(petrol_details,many=False)
        return Response(serializers.data)

class GasLogDetails(APIView):
    def get_gas_details(self,log_id):
        try:
            return Log.objects.all().filter(fuel_id=3).filter(pk=log_id).first()
        except Log.DoesNotExist:
            return Http404
    
    def get(self, request, log_id, format=None):
        today = dt.date.today()
        gas_details = Log.objects.all().filter(fuel_id=3).filter(pk=log_id).first()
        serializers = LogSerializer(gas_details,many=False)
        return Response(serializers.data)

class MpesaLogDetails(APIView):
    def get_mpesa_details(self,log_id):
        try:
            return LogMpesa.objects.all().filter(pk=log_id)
        except LogMpesa.DoesNotExist:
            return Http404
    
    def get(self, request, log_id, format=None):
        mpesa_details = LogMpesa.objects.all().filter(pk=log_id)
        serializers = LogMpesaSerializer(mpesa_details,many=False)
        return Response(serializers.data)

class PasLogs(APIView):
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