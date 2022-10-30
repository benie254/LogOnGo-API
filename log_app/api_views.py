import sendgrid
from sendgrid.helpers.mail import * 
import os 
from decouple import config 
from django.shortcuts import get_object_or_404, render,redirect 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from log_app.serializer import ContactSerializer, CreditCardReportSerializer, DeleteCreditRequestSerializer, DeleteLogRequestSerializer, DeleteMpesaRequestSerializer, FuelReceivedSerializer, FuelSerializer, FuelSummarySerializer, IncidentSerializer, LogCreditCardSerializer, LogMpesaSerializer, LogReportSerializer, LogSerializer, AnnouncementSerializer,LogReport, MpesaReportSerializer, PumpSerializer, LogSummarySerializer, PumpSummarySerializer


from django.http import HttpResponse,Http404, JsonResponse
from django.contrib.auth.decorators import login_required
from log_app.models import CreditCardReport, Fuel, FuelReceived, LogCreditCard, LogReport, MpesaReport, MyUser, Pump, Incident, Summary
import datetime as dt 
from django.db.models import Sum
from django.contrib import messages

from django.db.models import Max, Min,F, ExpressionWrapper, DecimalField, PositiveIntegerField

from log_app.models import Announcement, Contact, Incident, Log, LogMpesa
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator
from django.template.loader import render_to_string

# Create your views here.
class LatestAnnouncements(APIView):
    def get_three_announcements(self):
        try:
            return Announcement.objects.all().order_by('-date')[:3]
        except Announcement.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        announcement = Announcement.objects.all().order_by('-date')[:3]
        serializers = AnnouncementSerializer(announcement,many=True)
        return Response(serializers.data)

class AllAnnouncements(APIView):
    def get_announcements(self):
        try:
            return Announcement.objects.all().order_by('-date')
        except Announcement.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        announcement = Announcement.objects.all().order_by('-date')
        serializers = AnnouncementSerializer(announcement,many=True)
        return Response(serializers.data)

class AllFuels(APIView):
    def get_all_fuels(self):
        try:
            return Fuel.objects.all().order_by('-pk')
        except Fuel.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        fuuel_info = Fuel.objects.all().order_by('-pk')
        serializers = FuelSerializer(fuuel_info,many=True)
        return Response(serializers.data)

class FuelInfo(APIView):
    def get_fuel_info(self,fuel_id):
        try:
            return Fuel.objects.all().filter(pk=fuel_id).last()
        except Fuel.DoesNotExist:
            return Http404

    def get(self, request, fuel_id, format=None):
        fuel_info = Fuel.objects.all().filter(pk=fuel_id).last()
        serializers = FuelSerializer(fuel_info,many=False)
        return Response(serializers.data)

    def put(self, request, fuel_id, format=None):
        fuel_info = Fuel.objects.all().filter(id=fuel_id).last()
        serializers = FuelSerializer(fuel_info,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class PumpInfo(APIView):
    def get_pump_info(self,pump_id):
        try:
            return Pump.objects.all().filter(pk=pump_id).last()
        except Pump.DoesNotExist:
            return Http404

    def get(self, request, pump_id, format=None):
        pump_info = Pump.objects.all().filter(pk=pump_id).last()
        serializers = PumpSerializer(pump_info,many=False)
        return Response(serializers.data)

    def put(self, request, pump_id, format=None):
        pump_info = Pump.objects.all().filter(pk=pump_id).last()
        serializers = PumpSerializer(pump_info,request.data)
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
        all_logs = Log.objects.all().order_by('-first_logged')
        serializers = LogSerializer(all_logs,many=True)
        return Response(serializers.data)

class LogsToday(APIView):
    def get_today_logs(self):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).order_by('-date')
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        today_logs = Log.objects.all().filter(date=today).order_by('-date')
        serializers = LogSerializer(today_logs,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = LogSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogs(APIView):
    def get_user_logs(self,user_id):
        try:
            return Log.objects.all().filter(user=user_id).order_by('-date')
        except Log.DoesNotExist:
            return Http404

    def get(self, request, user_id, format=None):
        user_logs = Log.objects.all().filter(user_id_id=user_id).order_by('-date')
        serializers = LogSerializer(user_logs,many=True)
        return Response(serializers.data)

class FuelLogsToday(APIView):
    def get_today_fuel_logs(self,fuel_id,pump_id):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(date=today).filter(fuel_id=fuel_id).filter(pump_id=pump_id).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, fuel_id, pump_id, format=None):
        today = dt.date.today()
        yesterday = today - dt.timedelta(days=1)
        fuel_info = Fuel.objects.all().filter(id=fuel_id).last()
        pump_info = Pump.objects.all().filter(id=pump_id).last()
        if fuel_info and pump_info:
            price_per_litre = fuel_info.price_per_litre
            today_fuel_log = Log.objects.all().filter(date=today).filter(pump_id=pump_id).filter(fuel_id=fuel_id).first()
            yesterday_fuel_logs = Log.objects.all().filter(pump_id=pump_id).filter(fuel_id=fuel_id).filter(date=yesterday).first()
            fuel_received = FuelReceived.objects.all().filter(fuel_id=fuel_id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
            serializers = LogSerializer(today_fuel_log,many=False)
            if today_fuel_log:
                if yesterday_fuel_logs:
                    today_fuel_log.eod_reading_yesterday = yesterday_fuel_logs.eod_reading_lts
                    today_fuel_log.save()
                    eod_yesterday = today_fuel_log.eod_reading_yesterday
                    today_fuel_log.balance_yesterday = yesterday_fuel_logs.balance
                    today_fuel_log.save()
                    bal_yesterday = today_fuel_log.balance_yesterday 
                    today_fuel_log.balance = ExpressionWrapper((bal_yesterday) - F('total_litres_sold'),output_field=DecimalField())
                    today_fuel_log.total_litres_sold = ExpressionWrapper(F('eod_reading_lts')-F(eod_yesterday),output_field=DecimalField())
                    today_fuel_log.amount_earned_today = ExpressionWrapper(F('total_litres_sold') * (price_per_litre),output_field=PositiveIntegerField())
                    today_fuel_log.save()
                    today_fuel_log.refresh_from_db()
                    if today_fuel_log.balance and fuel_received:
                        received = fuel_received.litres_received
                        init_bal = today_fuel_log.balance
                        today_fuel_log.updated_balance = (init_bal) + (received)
                        today_fuel_log.save()
                        today_fuel_log.refresh_from_db()
                        updated_bal = today_fuel_log.updated_balance 
                    elif updated_bal and fuel_received:
                        today_fuel_log.updated_balance = (updated_bal) + (fuel_received)
                        today_fuel_log.save()
                        today_fuel_log.refresh_from_db()
                else:
                    today_fuel_log.total_litres_sold = ExpressionWrapper(F('eod_reading_lts')-F('eod_reading_yesterday'),output_field=DecimalField())
                    today_fuel_log.amount_earned_today = ExpressionWrapper(F('total_litres_sold') * (price_per_litre),output_field=PositiveIntegerField())
                    today_fuel_log.save()
                    total_sold = today_fuel_log.total_litres_sold
                    init = fuel_info.initial_litres_in_tank 
                    today_fuel_log.balance = (init) - (total_sold)
                    today_fuel_log.save()
                    today_fuel_log.refresh_from_db()
                    if today_fuel_log.balance and fuel_received:
                        received = fuel_received.litres_received
                        init_bal = today_fuel_log.balance
                        today_fuel_log.updated_balance = (init_bal) + (received)
                        today_fuel_log.save()
                        today_fuel_log.refresh_from_db()
                        updated_bal = today_fuel_log.updated_balance 
                    elif updated_bal and fuel_received:
                        today_fuel_log.updated_balance = (updated_bal) + (fuel_received)
                        today_fuel_log.save()
                        today_fuel_log.refresh_from_db()
                today_fuel_log.cumulative_litres_sold_today = today_fuel_log.aggregate(TOTAL = Sum('total_litres_sold'))['TOTAL']
                today_fuel_log.cumulative_amount_today = today_fuel_log.aggregate(TOTAL = Sum('amount_earned_today'))['TOTAL']
                if today_fuel_log.updated_balance:
                    today_fuel_log.cumulative_balance_today = today_fuel_log.aggregate(TOTAL = Sum('updated_balance'))['TOTAL']
                else:
                    today_fuel_log.cumulative_balance_today = today_fuel_log.aggregate(TOTAL = Sum('balance'))['TOTAL']
                return Response(serializers.data)
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_404_NOT_FOUND)

class PumpSummaryToday(APIView):
    def get_pump_summary(self,pump_id,fuel_id):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(fuel_id=fuel_id).filter(pump_id=pump_id).filter(date=today).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, pump_id, fuel_id, format=None):
        today = dt.date.today()
        pump_summary = Log.objects.all().filter(fuel_id=fuel_id).filter(pump_id=pump_id).filter(date=today).first()
        serializers = PumpSummarySerializer(pump_summary,many=False)
        return Response(serializers.data)
        
class FuelSummaryToday(APIView):
    def get_fuel_summary(self,fuel_id):
        today = dt.date.today()
        try:
            return Log.objects.all().filter(fuel_id=fuel_id).filter(date=today).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, fuel_id, format=None):
        today = dt.date.today()
        fuel_summary = Log.objects.all().filter(fuel_id=fuel_id).filter(date=today).first()
        serializers = FuelSummarySerializer(fuel_summary,many=False)
        return Response(serializers.data)

class AllMpesaLogs(APIView):
    def get_all_mpesa_logs(self):
        try:
            return LogMpesa.objects.all().order_by('-first_logged')
        except LogMpesa.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        all_mpesa_logs = LogMpesa.objects.all().order_by('-first_logged')
        serializers = LogMpesaSerializer(all_mpesa_logs,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = LogMpesaSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class AllCreditCardLogs(APIView):
    def get_all_credit_card_logs(self):
        try:
            return LogCreditCard.objects.all().order_by('-first_logged')
        except LogCreditCard.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        all_credit_card_logs = LogCreditCard.objects.all().order_by('-first_logged')
        serializers = LogMpesaSerializer(all_credit_card_logs,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = LogCreditCardSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class MpesaLogsToday(APIView):
    def get_today_mpesa_logs(self,fuel_id):
        today = dt.date.today()
        try:
            return LogMpesa.objects.all().filter(date=today).filter(fuel=fuel_id)
        except LogMpesa.DoesNotExist:
            return Http404

    def get(self, request, fuel_id, format=None):
        today = dt.date.today()
        first_mpesa_log = LogMpesa.objects.all().filter(date=today).filter(fuel=fuel_id).first()
        today_mpesa_logs = LogMpesa.objects.all().filter(date=today).filter(fuel=fuel_id)
        if first_mpesa_log:
            serializers = LogMpesaSerializer(today_mpesa_logs,many=True)
            return Response(serializers.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

class CreditCardLogsToday(APIView):
    def get_today_credit_card_logs(self,fuel_id):
        today = dt.date.today()
        try:
            return LogCreditCard.objects.all().filter(date=today).filter(fuel=fuel_id)
        except LogCreditCard.DoesNotExist:
            return Http404

    def get(self, request, fuel_id, format=None):
        today = dt.date.today()
        first_credit_card_log = LogCreditCard.objects.all().filter(date=today).filter(fuel=fuel_id).first()
        today_credit_card_logs = LogCreditCard.objects.all().filter(date=today).filter(fuel=fuel_id)
        if first_credit_card_log:
            serializers = LogCreditCardSerializer(today_credit_card_logs,many=True)
            return Response(serializers.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

class UserMpesaLogs(APIView):
    def get_user_mpesa_logs(self,user_id):
        try:
            return LogMpesa.objects.all().filter(user=user_id).order_by('-first_logged')
        except LogMpesa.DoesNotExist:
            return Http404

    def get(self, request, user_id, format=None):
        user_mpesa_logs = LogMpesa.objects.all().filter(user=user_id).order_by('-first_logged')
        serializers = LogMpesaSerializer(user_mpesa_logs,many=True)
        return Response(serializers.data)

class UserCreditCardLogs(APIView):
    def get_user_credit_card_logs(self,user_id):
        try:
            return LogCreditCard.objects.all().filter(user=user_id).order_by('-first_logged')
        except LogCreditCard.DoesNotExist:
            return Http404

    def get(self, request, user_id, format=None):
        user_credit_card_logs = LogCreditCard.objects.all().filter(user=user_id).order_by('-first_logged')
        serializers = LogCreditCardSerializer(user_credit_card_logs,many=True)
        return Response(serializers.data)

class AllFuelReceivedToday(APIView):
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
    def get_fuel_received_info(self,log_id):
        log_details = Log.objects.all().filter(pk=log_id).first() 
        if log_details:
            log_date = log_details.date
            fuel_id = log_details.fuel
            try:
                return FuelReceived.objects.all().filter(fuel_id=fuel_id).filter(date_received=log_date)
            except FuelReceived.DoesNotExist:
                return Http404
        else:
            Http404
    
    def get(self, request, log_id, format=None):
        today = dt.date.today()
        log_details = Log.objects.all().filter(pk=log_id).first() 
        if log_details:
            log_date = log_details.date
            fuel_id = log_details.fuel
            fuel_received_info = FuelReceived.objects.all().filter(fuel_id=fuel_id).filter(date_received=log_date)
            serializers = FuelReceivedSerializer(fuel_received_info,many=True)
            return Response(serializers.data)
        else:
            fuel_id = log_id 
            fuel_received_info = FuelReceived.objects.all().filter(fuel_id=fuel_id).filter(date_received=today)
            serializers = FuelReceivedSerializer(fuel_received_info,many=True)
            return Response(serializers.data)

class TotalFuelReceivedToday(APIView):
    def get_fuel_received_info(self,log_id):
        log_details = Log.objects.all().filter(id=log_id).first() 
        if log_details:
            log_date = log_details.date
            fuel_id = log_details.fuel
            try:
                return FuelReceived.objects.all().filter(fuel_id=fuel_id).filter(date_received=log_date).first()
            except FuelReceived.DoesNotExist:
                return Http404
        else:
            Http404
    
    def get(self, request, log_id, format=None):
        today = dt.date.today()
        log_details = Log.objects.all().filter(id=log_id).first() 
        if log_details:
            log_date = log_details.date
            fuel_id = log_details.fuel
            first_fuel_received = FuelReceived.objects.all().filter(fuel_id=fuel_id).filter(date_received=log_date).first()
            fuel_received_info = FuelReceived.objects.all().filter(fuel_id=fuel_id).filter(date_received=log_date)
            if first_fuel_received:
                first_fuel_received.total_fuel_received_today = fuel_received_info.aggregate(TOTAL = Sum('litres_received'))['TOTAL']
                first_fuel_received.save()
                first_fuel_received.refresh_from_db()
                serializers = FuelReceivedSerializer(fuel_received_info,many=False)
                return Response(serializers.data)
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            fuel_id = log_id 
            first_fuel_received = FuelReceived.objects.all().filter(fuel_id=fuel_id).filter(date_received=today).first()
            fuel_received_info = FuelReceived.objects.all().filter(fuel_id=fuel_id).filter(date_received=today)
            if first_fuel_received:
                first_fuel_received.total_fuel_received_today = fuel_received_info.aggregate(TOTAL = Sum('litres_received'))['TOTAL']
                first_fuel_received.save()
                first_fuel_received.refresh_from_db()
                serializers = FuelReceivedSerializer(fuel_received_info,many=False)
                return Response(serializers.data)
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class LogDetails(APIView):
    def get_log_details(self,log_id):
        try:
            return Log.objects.all().filter(pk=log_id).first()
        except Log.DoesNotExist:
            return Http404
    
    def get(self, request, log_id, format=None):
        log_details = Log.objects.all().filter(pk=log_id).first()
        serializers = LogSerializer(log_details,many=False)
        return Response(serializers.data)

    def put(self, request, log_id, format=None):
        log_details = Log.objects.all().filter(pk=log_id).first()
        serializers = LogSerializer(log_details,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class MpesaLogDetails(APIView):
    def get_mpesa_details(self,id):
        try:
            return LogMpesa.objects.all().filter(id=id).last()
        except LogMpesa.DoesNotExist:
            return Http404
    
    def get(self, request, id, format=None):
        mpesa_details = LogMpesa.objects.all().filter(id=id).last()
        if mpesa_details:
            mpesa_date = mpesa_details.date
            mpesa_details.daily_total = LogMpesa.objects.all().filter(date=mpesa_date).aggregate(TOTAL = Sum('amount'))['TOTAL']
            mpesa_details.cumulative_amount = LogMpesa.objects.all().aggregate(TOTAL = Sum('amount'))['TOTAL']
            mpesa_details.save()
            mpesa_details.refresh_from_db()
            serializers = LogMpesaSerializer(mpesa_details,many=False)
            return Response(serializers.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, format=None):
        mpesa_details = LogMpesa.objects.all().filter(id=id).first()
        serializers = LogMpesaSerializer(mpesa_details,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class CreditCardLogDetails(APIView):
    
    def get_credit_card_details(self,id):
        try:
            return LogCreditCard.objects.all().filter(id=id).last()
        except LogCreditCard.DoesNotExist:
            return Http404
    
    def get(self, request, id, format=None):
        credit_card_details = LogCreditCard.objects.all().filter(id=id).last()
        if credit_card_details:
            credit_card_date = credit_card_details.date
            credit_card_details.daily_total = LogCreditCard.objects.all().filter(date=credit_card_date).aggregate(TOTAL = Sum('amount'))['TOTAL']
            credit_card_details.cumulative_amount = LogCreditCard.objects.all().aggregate(TOTAL = Sum('amount'))['TOTAL']
            credit_card_details.save()
            credit_card_details.refresh_from_db()
            serializers = LogCreditCardSerializer(credit_card_details,many=False)
            return Response(serializers.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id, format=None):
        credit_card_details = LogCreditCard.objects.all().filter(id=id).first()
        serializers = LogCreditCardSerializer(credit_card_details,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class PastLogs(APIView):
    def get(self,request,past_date):
        try:
        # convert data from the string url
            date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

        except ValueError:
            # raise 404 when value error is thrown
            raise Http404()
            assert False

        if date == dt.date.today():
            today = dt.date.today()
            past_logs = Log.objects.filter(date=today)
            serializers = LogSerializer(past_logs,many=True)
            return Response(serializers.data)

        past_logs = Log.objects.filter(date=date)
        serializers = LogSerializer(past_logs,many=True)
        return Response(serializers.data)

class PastMpesaLogs(APIView):
    
    
    def get(self,request,past_date):
        try:
        # convert data from the string url
            date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

        except ValueError:
            # raise 404 when value error is thrown
            raise Http404()
            assert False

        if date == dt.date.today():
            today = dt.date.today()
            past_mpesa_logs = LogMpesa.objects.filter(date=today)
            serializers = LogMpesaSerializer(past_mpesa_logs,many=True)
            return Response(serializers.data)

        past_mpesa_logs = LogMpesa.objects.filter(date=date)
        serializers = LogMpesaSerializer(past_mpesa_logs,many=True)
        return Response(serializers.data)

class PastCreditCardLogs(APIView):
    
    
    def get(self,request,past_date):
        try:
        # convert data from the string url
            date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

        except ValueError:
            # raise 404 when value error is thrown
            raise Http404()
            assert False

        if date == dt.date.today():
            today = dt.date.today()
            past_credit_card_logs = LogCreditCard.objects.filter(date=today)
            serializers = LogCreditCardSerializer(past_credit_card_logs,many=True)
            return Response(serializers.data)

        past_credit_card_logs = LogCreditCard.objects.filter(date=date)
        serializers = LogCreditCardSerializer(past_credit_card_logs,many=True)
        return Response(serializers.data)

class EmailReport(APIView):
    
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

class EmailCreditCardReport(APIView):
    
    def get_credit_card_reports(self):
        try:
            return CreditCardReport.objects.all()
        except CreditCardReport.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        reports = CreditCardReport.objects.all()
        serializers = CreditCardReportSerializer(reports,many=True)
        return Response(serializers.data)

    def post(self, request,format=None):
        serializers = CreditCardReportSerializer(data=request.data)
        if serializers.is_valid():
            # serializer.is_valid(raise_exception=True)
            date=serializers.validated_data['date']
            card_name=serializers.validated_data['card_name']
            card_number=serializers.validated_data['card_number']
            amount=serializers.validated_data['amount']
            daily_total=serializers.validated_data['daily_total']
            cumulative_amount=serializers.validated_data['cumulative_amount']
            
            logged_by=serializers.validated_data['logged_by']
            username=serializers.validated_data['admin_name']
            receiver=serializers.validated_data['admin_email']
            serializers.save()
            
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = "Here is your requested email report:</p> <br> <ul><li>date: " + str(date) + " </li><li>card name.: " + str(card_name) + "</li><li>card number: " + str(card_number) + " </li><li>amount: " + str(amount) + "</li><li>daily total: " + str(daily_total) + "</li><li>cumulative amount: " + str(cumulative_amount) + "</li><li>logged by: " + str(logged_by) + "</li></ul> <br> <small> The data committee, <br> LogOnGo. <br> ©Pebo Kenya Ltd  </small>"
            message = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = receiver,
                subject = "Your CreditCard report",
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
    


class DeleteLogRequest(APIView):
    def post(self, request):
        serializer = DeleteLogRequestSerializer(data=request.data)
        if serializer.is_valid():
            log_id = request.data['log_id']
            date = request.data['date']
            date_requested = request.data['date_requested']
            eod = request.data['eod_reading_lts']
            eod_yesterday = request.data['eod_reading_yesterday']
            litres_sold = request.data['litres_sold_today']
            amount = request.data['amount']
            logged_by = request.data['logged_by']
            receiver='fullstack.benie@gmail.com'
            username='Janja'
            requested_by = request.data['requested_by']
            serializer.save()
            myHtml = render_to_string('email/delete-log-request.html', {
                'log_id':log_id,
                'date':date,
                'date_requested':date_requested,
                'eod':eod,
                'eod_yesterday':eod_yesterday,
                'litres_sold':litres_sold,
                'amount':amount,
                'username':username,
                'logged_by':logged_by,
                'requested_by':requested_by,
            })
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            message = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = receiver,
                subject = "Delete Request: General Log",
                html_content= myHtml
            )
            print(message)
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
                'message': 'Delete request sent to the admin.',
                }
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DeleteMpesaRequest(APIView):
    def post(self, request):
        serializer = DeleteMpesaRequestSerializer(data=request.data)
        if serializer.is_valid():
            log_id = request.data['log_id']
            date = request.data['date']
            date_requested = request.data['date_requested']
            transaction = request.data['transaction_number']
            bank = request.data['amount_transferred_to_bank']
            amount = request.data['amount']
            customer_name = request.data['customer_name']
            customer_no = request.data['customer_phone_number']
            logged_by = request.data['logged_by']
            requested_by = request.data['requested_by']
            serializer.save()
            receiver='fullstack.benie@gmail.com'
            username='Janja'
            myHtml = render_to_string('email/delete-mpesa-request.html', {
                'log_id':log_id,
                'date':date,
                'date_requested':date_requested,
                'transaction':transaction,
                'bank':bank,
                'amount':amount,
                'customer_name':customer_name,
                'customer_no':customer_no,
                'username':username,
                'logged_by':logged_by,
                'requested_by':requested_by,
            })
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            message = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = receiver,
                subject = "Delete Request: Mpesa Log",
                html_content= myHtml
            )
            print(message)
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
                'message': 'Delete request sent to the admin.',
                }
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DeleteCreditCardRequest(APIView):
    def post(self, request):
        serializer = DeleteCreditRequestSerializer(data=request.data)
        if serializer.is_valid():
            log_id = request.data['log_id']
            date = request.data['date']
            date_requested = request.data['date_requested']
            card_name = request.data['card_name']
            card_no = request.data['card_number']
            amount = request.data['amount']
            logged_by = request.data['logged_by']
            requested_by = request.data['requested_by']
            serializer.save()
            receiver='fullstack.benie@gmail.com'
            username='Janja'
            myHtml = render_to_string('email/delete-credit-request.html', {
                'log_id':log_id,
                'date':date,
                'date_requested':date_requested,
                'card_name':card_name,
                'card_no':card_no,
                'amount':amount,
                'username':username,
                'logged_by':logged_by,
                'requested_by':requested_by,
            })
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            message = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = receiver,
                subject = "Delete Request: Credit Card",
                html_content= myHtml
            )
            print(message)
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
                'message': 'Delete request sent to the admin.',
                }
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)