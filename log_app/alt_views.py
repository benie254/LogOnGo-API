import sendgrid
from sendgrid.helpers.mail import * 
import os 
from decouple import config 
from django.shortcuts import get_object_or_404, render,redirect 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from log_app.serializer import FuelReceivedSerializer, FuelSerializer, LogMpesaSerializer, LogReportSerializer, LogSerializer, AnnouncementSerializer,LogReport, MpesaReportSerializer


from django.http import HttpResponse,Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from log_app.models import Fuel, FuelReceived, LogReport, MpesaReport, MyUser, Pump 
import datetime as dt 
from django.db.models import Sum
from django.contrib import messages

from django.db.models import Max, Min,F, ExpressionWrapper, DecimalField, PositiveIntegerField

from log_app.models import Announcement, Contact, Incident, Log, LogMpesa
from rest_framework.permissions import AllowAny,AllowAny


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
        pump_one_init = pump_one.initial_litres_in_tank
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
            if yesterday_fuel_logs.balance and today_fuel_log.total_litres_sold:
                pump_one.balance_yesterday = yesterday_fuel_logs.balance
                pump_one.save()
                pump_one.refresh_from_db()
                bal_yesterday = pump_one.balance_yesterday
                total_sold = today_fuel_log.total_litres_sold
                pump_one.balance = (bal_yesterday) - (total_sold)
                pump_one.save()
                pump_one.refresh_from_db()
                bal = today_fuel_log.balance 
            elif pump_one.balance_yesterday:
                bal_yesterday = pump_one.balance_yesterday
                total_sold = today_fuel_log.total_litres_sold
                pump_one.balance = (bal_yesterday) - (total_sold)
                pump_one.save()
                pump_one.refresh_from_db()
                bal = today_fuel_log.balance 
            elif today_fuel_log.total_litres_sold:
                init = pump_one_init
                total_sold = today_fuel_log.total_litres_sold
                pump_one.balance = (init) - (total_sold)
                pump_one.save()
                pump_one.refresh_from_db()
        else: 
            Http404
        serializers = LogSerializer(today_fuel_log,many=False)
        return Response(serializers.data)