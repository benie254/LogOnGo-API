from log_app.serializer import (
    ContactSerializer, CreditCardReportSerializer, DeleteCreditRequestSerializer, DeleteLogRequestSerializer, DeleteMpesaRequestSerializer, 
    FuelReceivedSerializer, FuelSerializer, IncidentSerializer, LogCreditCardSerializer, LogMpesaSerializer, LogReportSerializer, LogSerializer, 
    AnnouncementSerializer,LogReport, MpesaReportSerializer, FuelSummarySerializer
)
from log_app.models import CreditCardReport, Fuel, FuelReceived, LogCreditCard, LogReport, MpesaReport, Incident

import sendgrid
from sendgrid.helpers.mail import * 
from decouple import config 
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
import datetime as dt 
from django.db.models import Sum
from django.db.models import F, ExpressionWrapper, DecimalField, PositiveIntegerField
from log_app.models import Announcement, Contact, Incident, Log, LogMpesa
from django.template.loader import render_to_string

from rest_framework.decorators import api_view, renderer_classes, permission_classes


# Create your views here.
@permission_classes([IsAuthenticated,])
class LatestAnnouncements(APIView):
    def get(self, request, format=None):
        announcement = Announcement.objects.all().order_by('-date')[:3]
        serializers = AnnouncementSerializer(announcement,many=True)
        return Response(serializers.data)

@permission_classes([IsAuthenticated,])
class AllAnnouncements(APIView):
    def get(self, request, format=None):
        announcement = Announcement.objects.all().order_by('-date')
        serializers = AnnouncementSerializer(announcement,many=True)
        return Response(serializers.data)

@permission_classes([IsAdminUser,])
class AddAnnouncements(APIView):
    def post(self, request, format=None):
        serializers = AnnouncementSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAdminUser,])
class UpdateAnnouncement(APIView):
    def get(self, request, id, format=None):
        announce = Announcement.objects.all().filter(pk=id).last()
        serializers = AnnouncementSerializer(announce,many=False)
        return Response(serializers.data)
    
    def put(self, request, id, format=None):
        announcement = Announcement.objects.all().filter(pk=id).last()
        serializers = AnnouncementSerializer(announcement,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        announcement = Announcement.objects.all().filter(pk=id).last()
        announcement.delete()
        return Response(status=status.HTTP_200_OK) 

@permission_classes([IsAuthenticated,])
class AllFuels(APIView):
    def get(self, request, format=None):
        fuuel_info = Fuel.objects.all().order_by('-pk')[:3]
        serializers = FuelSerializer(fuuel_info,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = FuelSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated,])
class FuelInfo(APIView):
    def get(self, request, fuel_id, format=None):
        fuel_info = Fuel.objects.all().filter(pk=fuel_id).last()
        serializers = FuelSerializer(fuel_info,many=False)
        return Response(serializers.data)

    def put(self, request, fuel_id, format=None):
        fuel_info = Fuel.objects.all().filter(pk=fuel_id).last()
        serializers = FuelSerializer(fuel_info,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAdminUser,])
class RemoveFuel(APIView):
    def delete(self, request, id, format=None):
        contact = Fuel.objects.all().filter(pk=id).last()
        contact.delete()
        return Response(status=status.HTTP_200_OK) 

@permission_classes([IsAuthenticated,])
class PetrolInfo(APIView):
    def get(self, request, format=None):
        fuel_info = Fuel.objects.all().filter(fuel_type='Petrol').last()
        serializers = FuelSerializer(fuel_info,many=False)
        return Response(serializers.data)

@permission_classes([IsAuthenticated,])
class DieselInfo(APIView):
    def get(self, request, format=None):
        fuel_info = Fuel.objects.all().filter(fuel_type='Diesel').last()
        serializers = FuelSerializer(fuel_info,many=False)
        return Response(serializers.data)

@permission_classes([IsAuthenticated,])
class GasInfo(APIView):
    def get(self, request, format=None):
        fuel_info = Fuel.objects.all().filter(fuel_type='Gas').last()
        serializers = FuelSerializer(fuel_info,many=False)
        return Response(serializers.data)

@permission_classes([IsAuthenticated,])
class AllFuelReceivedToday(APIView):
    def get(self, request, format=None):
        today = dt.date.today()
        fuel_received_today = FuelReceived.objects.all().filter(date=today)
        serializers = FuelReceivedSerializer(fuel_received_today,many=True)
        return Response(serializers.data)
    
    def post(self, request, format=None):
        serializers = FuelReceivedSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated,])
class FuelReceivedTodayInfo(APIView):
    def get(self, request, fuel_id, format=None):
        today = dt.date.today()
        fuel_rcvd = FuelReceived.objects.all().filter(date=today).filter(fuel_id=fuel_id)
        last_fuel_rcvd = FuelReceived.objects.all().filter(fuel_id=fuel_id).filter(date=today).last()
        if last_fuel_rcvd:
            last_fuel_rcvd.total_td = fuel_rcvd.aggregate(TOTAL = Sum('litres'))['TOTAL']
            last_fuel_rcvd.save()
            last_fuel_rcvd.refresh_from_db()
            serializers = FuelReceivedSerializer(fuel_rcvd,many=True)
            return Response(serializers.data)
        return Response(status.HTTP_204_NO_CONTENT)

@permission_classes([IsAdminUser,])
class FuelReceivedDetails(APIView):
    def get(self, request, id, format=None):
        fuel_received = FuelReceived.objects.all().filter(pk=id).first()
        serializers = FuelReceivedSerializer(fuel_received,many=False)
        return Response(serializers.data)
    
    def put(self, request, id, format=None):
        fuel_info = FuelReceived.objects.all().filter(pk=id).last()
        serializers = FuelReceivedSerializer(fuel_info,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, format=None):
        contact = Fuel.objects.all().filter(pk=id).last()
        contact.delete()
        return Response(status=status.HTTP_200_OK) 

@permission_classes([IsAuthenticated,])
class TotalFuelReceivedToday(APIView):
    def get(self, request, fuel_id, format=None):
        today = dt.date.today()
        fuel_rcvd = FuelReceived.objects.all().filter(date=today).filter(fuel_id=fuel_id).last()
        serializers = FuelReceivedSerializer(fuel_rcvd,many=False)
        return Response(serializers.data)

@permission_classes([IsAuthenticated,])
class AllLogs(APIView):
    def get(self, request, format=None):
        all_logs = Log.objects.all().order_by('-first_logged')
        serializers = LogSerializer(all_logs,many=True)
        return Response(serializers.data)

@permission_classes([IsAuthenticated,])
class LogsToday(APIView):
    def get(self, request, format=None):
        today = dt.date.today()
        today_logs = Log.objects.all().filter(date=today).order_by('-date')
        serializers = LogSerializer(today_logs,many=True)
        return Response(serializers.data)
    
    def post(self, request, format=None):
        serializers = LogSerializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated,])
class UserLogs(APIView):
    def get(self, request, user_id, format=None):
        user_logs = Log.objects.all().filter(user=user_id).order_by('-first_logged')
        if user_logs:
            serializers = LogSerializer(user_logs,many=True)
            return Response(serializers.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticated,])
class FuelLogsToday(APIView):
    def get(self, request, fuel_id, format=None):
        today = dt.date.today()
        yesterday = today - dt.timedelta(days=1)
        fuel_info = Fuel.objects.all().filter(pk=fuel_id).last()
        if fuel_info:
            pp_litre = fuel_info.pp_litre
            logs = Log.objects.all().filter(date=today).filter(fuel_id=fuel_id).last()
            logs_today = Log.objects.all().filter(date=today).filter(fuel_id=fuel_id)
            logs_yesterday = Log.objects.all().filter(date=yesterday).filter(fuel_id=fuel_id).last()
            if logs:
                serializers = LogSerializer(logs_today,many=True)
                logs.litres_sold = ExpressionWrapper(F('eod_reading') - F('eod_yesterday'),output_field=DecimalField())
                logs.save()
                logs.refresh_from_db()
                logs.amount_td = ExpressionWrapper(F('litres_sold') * (pp_litre),output_field=PositiveIntegerField())
                logs.save()
                logs.refresh_from_db()   
                if logs_yesterday:
                    logs.bal = ExpressionWrapper(F('bal_yesterday') - F('litres_sold'),output_field=DecimalField())
                    logs.save()
                    logs.refresh_from_db()  
                else:
                    tank_init = logs.fuel.tank_init
                    logs.bal = ExpressionWrapper((tank_init) - ('litres_sold'),output_field=PositiveIntegerField())
                    logs.save()
                    logs.refresh_from_db()  
                date = logs.date  
                fuel_received = FuelReceived.objects.all().filter(fuel_id=fuel_id).filter(date=date).aggregate(TOTAL = Sum('litres'))['TOTAL']
                fuel_td = FuelReceived.objects.all().filter(fuel_id=fuel_id).filter(date=date).last()
                if logs.bal and fuel_td:
                    bal = logs.bal
                    received = fuel_td.litres
                    init_bal = bal
                    logs.updated_bal = (init_bal) + (received)
                    logs.save()
                    logs.refresh_from_db()
                elif logs.updated_bal and fuel_received:
                    updated_bal = logs.updated_bal
                    updated_bal = (updated_bal) + (fuel_received)
                if logs.updated_bal:
                    logs.cumulative_bal_td = logs_today.aggregate(TOTAL = Sum('updated_bal'))['TOTAL']
                    logs.save()
                    logs.refresh_from_db()
                elif logs.bal:
                    logs.cumulative_bal_td = logs_today.aggregate(TOTAL = Sum('bal'))['TOTAL']
                    logs.save()
                    logs.refresh_from_db()
                if logs.litres_sold:
                    logs.cumulative_litres_td = logs_today.aggregate(TOTAL = Sum('litres_sold'))['TOTAL']
                    logs.save()
                    logs.refresh_from_db()
                if logs.amount_td:
                    logs.cumulative_amount_td = logs_today.aggregate(TOTAL = Sum('amount_td'))['TOTAL']
                    logs.save()
                    logs.refresh_from_db()
                return Response(serializers.data)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes([IsAuthenticated,])
class FuelLogsYesterday(APIView):
    def get(self, request, fuel_id, format=None):
        today = dt.date.today()
        yesterday = today - dt.timedelta(days=1)
        logs = Log.objects.all().filter(date=yesterday).filter(fuel_id=fuel_id).last()
        if logs:
            serializers = LogSerializer(logs,many=False)
            return Response(serializers.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticated,])     
class FuelSummaryToday(APIView):
    def get(self, request, fuel_id, format=None):
        today = dt.date.today()
        fuel_summary = Log.objects.all().filter(fuel_id=fuel_id).filter(date=today).last()
        if fuel_summary:
            serializers = FuelSummarySerializer(fuel_summary,many=False)
            return Response(serializers.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes([IsAuthenticated,])
class AllMpesaLogs(APIView):
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

@permission_classes([IsAuthenticated,])
class MpesaLogsToday(APIView):
    def get(self, request, fuel_id, format=None):
        today = dt.date.today()
        today_mpesa_logs = LogMpesa.objects.all().filter(date=today).filter(fuel=fuel_id)
        last_mpesa_log = LogMpesa.objects.all().filter(date=today).filter(fuel=fuel_id).last()
        if last_mpesa_log:
            mpesa_date = last_mpesa_log.date
            last_mpesa_log.fuel_type = last_mpesa_log.fuel.fuel_type
            last_mpesa_log.pp_litre = last_mpesa_log.fuel.pp_litre
            last_mpesa_log.save()
            last_mpesa_log.refresh_from_db()
            last_mpesa_log.total_td = LogMpesa.objects.all().filter(date=mpesa_date).aggregate(TOTAL = Sum('amount'))['TOTAL']
            last_mpesa_log.cumulative_amount = LogMpesa.objects.all().aggregate(TOTAL = Sum('amount'))['TOTAL']
            last_mpesa_log.save()
            last_mpesa_log.refresh_from_db()
            serializers = LogMpesaSerializer(today_mpesa_logs,many=True)
            return Response(serializers.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes([IsAuthenticated,])
class UserMpesaLogs(APIView):
    def get(self, request, user_id, format=None):
        user_mpesa_logs = LogMpesa.objects.all().filter(user=user_id).order_by('-first_logged')
        if user_mpesa_logs:
            serializers = LogMpesaSerializer(user_mpesa_logs,many=True)
            return Response(serializers.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticated,])
class AllCreditCardLogs(APIView):
    def get(self, request, format=None):
        all_credit_card_logs = LogCreditCard.objects.all().order_by('-first_logged')
        serializers = LogCreditCardSerializer(all_credit_card_logs,many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = LogCreditCardSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated,])
class CreditCardLogsToday(APIView):
    def get(self, request, fuel_id, format=None):
        today = dt.date.today()
        last_credit_card_log = LogCreditCard.objects.all().filter(date=today).filter(fuel=fuel_id).last()
        today_credit_card_logs = LogCreditCard.objects.all().filter(date=today).filter(fuel=fuel_id)
        if last_credit_card_log:
            credit_card_date = last_credit_card_log.date
            last_credit_card_log.fuel_type = last_credit_card_log.fuel.fuel_type
            last_credit_card_log.pp_litre = last_credit_card_log.fuel.pp_litre
            last_credit_card_log.save()
            last_credit_card_log.refresh_from_db()
            last_credit_card_log.total_td = LogCreditCard.objects.all().filter(date=credit_card_date).aggregate(TOTAL = Sum('amount'))['TOTAL']
            last_credit_card_log.cumulative_amount = LogCreditCard.objects.all().aggregate(TOTAL = Sum('amount'))['TOTAL']
            last_credit_card_log.save()
            last_credit_card_log.refresh_from_db()
            serializers = LogCreditCardSerializer(today_credit_card_logs,many=True)
            return Response(serializers.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

@permission_classes([IsAuthenticated,])
class UserCreditCardLogs(APIView):
    def get(self, request, user_id, format=None):
        user_credit_card_logs = LogCreditCard.objects.all().filter(user=user_id).order_by('-first_logged')
        if user_credit_card_logs:
            serializers = LogCreditCardSerializer(user_credit_card_logs,many=True)
            return Response(serializers.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticated,])
class LogDetails(APIView):
    def get(self, request, log_id, format=None):
        log_details = Log.objects.all().filter(pk=log_id).first()
        serializers = LogSerializer(log_details,many=False)
        log_details.fuel_type = log_details.fuel.fuel_type
        log_details.pp_litre = log_details.fuel.pp_litre 
        log_details.save()
        log_details.refresh_from_db()
        log_details.litres_sold = ExpressionWrapper(F('eod_reading') - F('eod_yesterday'),output_field=DecimalField())
        log_details.save()
        log_details.refresh_from_db()
        log_details.amount_td = ExpressionWrapper(F('litres_sold') * F('pp_litre'),output_field=PositiveIntegerField())
        log_details.save()
        log_details.refresh_from_db() 
        log_date = log_details.date 
        yesterday = log_date - dt.timedelta(days=1)
        f_id = log_details.fuel.id
        logs_yesterday = Log.objects.all().filter(date=yesterday).filter(fuel=f_id).last()
        if logs_yesterday:
            log_details.bal = ExpressionWrapper(F('bal_yesterday') - F('litres_sold'),output_field=DecimalField())
            log_details.save()
            log_details.refresh_from_db()  
        else:
            tank_init = log_details.fuel.tank_init
            log_details.bal = ExpressionWrapper((tank_init) - ('litres_sold'),output_field=PositiveIntegerField())
            log_details.save()
            log_details.refresh_from_db()    
        date = log_details.date  
        fuel_id = log_details.fuel
        fuel_received = FuelReceived.objects.all().filter(fuel_id=fuel_id).filter(date=date).aggregate(TOTAL = Sum('litres'))['TOTAL']
        last_received = FuelReceived.objects.all().filter(fuel_id=fuel_id).filter(date=date).last()
        logs_today = Log.objects.all().filter(date=date)
        if log_details.bal and fuel_received:
            bal = log_details.bal
            received = last_received.litres
            init_bal = bal
            log_details.updated_bal = (init_bal) + (received)
            log_details.save()
            log_details.refresh_from_db()
        elif log_details.updated_bal and fuel_received:
            updated_bal = log_details.updated_bal
            updated_bal = (updated_bal) + (fuel_received)
        if log_details.updated_bal:
            log_details.cumulative_bal_td = logs_today.aggregate(TOTAL = Sum('updated_bal'))['TOTAL']
            log_details.save()
            log_details.refresh_from_db()
        elif log_details.bal:
            log_details.cumulative_bal_td = logs_today.aggregate(TOTAL = Sum('bal'))['TOTAL']
            log_details.save()
            log_details.refresh_from_db()
        if log_details.litres_sold:
            log_details.cumulative_litres_td = logs_today.aggregate(TOTAL = Sum('litres_sold'))['TOTAL']
            log_details.save()
            log_details.refresh_from_db()
        if log_details.amount_td:
            log_details.cumulative_amount_td = logs_today.aggregate(TOTAL = Sum('amount_td'))['TOTAL']
            log_details.save()
            log_details.refresh_from_db()
        return Response(serializers.data)
    
    def put(self, request, log_id, format=None):
        log_details = Log.objects.all().filter(pk=log_id).first()
        serializers = LogSerializer(log_details,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAdminUser,])
class RemoveLog(APIView):
    def delete(self, request, id, format=None):
        contact = Log.objects.all().filter(pk=id).last()
        contact.delete()
        return Response(status=status.HTTP_200_OK) 

@permission_classes([IsAuthenticated,])
class MpesaLogDetails(APIView):
    def get(self, request, id, format=None):
        mpesa_details = LogMpesa.objects.all().filter(id=id).last()
        if mpesa_details:
            mpesa_date = mpesa_details.date
            mpesa_details.fuel_type = mpesa_details.fuel.fuel_type
            mpesa_details.pp_litre = mpesa_details.fuel.pp_litre
            mpesa_details.save()
            mpesa_details.refresh_from_db()
            mpesa_details.total_td = LogMpesa.objects.all().filter(date=mpesa_date).aggregate(TOTAL = Sum('amount'))['TOTAL']
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

@permission_classes([IsAdminUser,])
class RemoveMpesa(APIView):
    def delete(self, request, id, format=None):
        contact = LogMpesa.objects.all().filter(pk=id).last()
        contact.delete()
        return Response(status=status.HTTP_200_OK) 

@permission_classes([IsAuthenticated,])
class CreditCardLogDetails(APIView):
    def get(self, request, id, format=None):
        credit_card_details = LogCreditCard.objects.all().filter(pk=id).last()
        if credit_card_details:
            credit_card_date = credit_card_details.date
            credit_card_details.fuel_type = credit_card_details.fuel.fuel_type
            credit_card_details.pp_litre = credit_card_details.fuel.pp_litre
            credit_card_details.save()
            credit_card_details.refresh_from_db()
            credit_card_details.total_td = LogCreditCard.objects.all().filter(date=credit_card_date).aggregate(TOTAL = Sum('amount'))['TOTAL']
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

@permission_classes([IsAdminUser,])
class RemoveCard(APIView):
    def delete(self, request, id, format=None):
        contact = LogCreditCard.objects.all().filter(pk=id).last()
        contact.delete()
        return Response(status=status.HTTP_200_OK) 

@permission_classes([IsAuthenticated,])
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

@permission_classes([IsAuthenticated,])
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

@permission_classes([IsAuthenticated,])
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

@permission_classes([IsAuthenticated,])
class EmailReport(APIView):
    def get(self, request, format=None):
        reports = LogReport.objects.all()
        serializers = LogSerializer(reports,many=True)
        return Response(serializers.data)

    def post(self, request,format=None):
        serializers = LogReportSerializer(data=request.data)
        if serializers.is_valid():
            # serializer.is_valid(raise_exception=True)
            eod_reading=serializers.validated_data['eod_reading']
            eod_yesterday=serializers.validated_data['eod_yesterday']
            litres_sold=serializers.validated_data['litres_sold']
            amount_td=serializers.validated_data['amount_td']
            bal=serializers.validated_data['bal']
            username=serializers.validated_data['name']
            receiver=serializers.validated_data['email']
            serializers.save()
            
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = "Here is your requested email report:</p> <br> <ul><li>eod: " + str(eod_reading) + " </li>eod_yesterday: " + str(eod_yesterday) + " <li>litres sold: " + str(litres_sold) + " </li>amount: " + str(amount_td) + " <li>bal: " + str(bal) + "</li></ul> <br> <small> The data committee, <br> LogOnGo. <br> ©Pebo Kenya Ltd  </small>"
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
    
@permission_classes([IsAuthenticated,])
class EmailMpesaReport(APIView):
    def get(self, request, format=None):
        reports = MpesaReport.objects.all()
        serializers = MpesaReportSerializer(reports,many=True)
        return Response(serializers.data)
    
    def post(self, request,format=None):
        serializers = MpesaReportSerializer(data=request.data)
        if serializers.is_valid():
            # serializer.is_valid(raise_exception=True)
            date=serializers.validated_data['date']
            transaction_no=serializers.validated_data['transaction_no']
            customer=serializers.validated_data['customer']
            customer_no=serializers.validated_data['customer_no']
            amount=serializers.validated_data['amount']
            to_bank=serializers.validated_data['to_bank']
            total_td=serializers.validated_data['total_td']
            cumulative_amount=serializers.validated_data['cumulative_amount']
            logged_by=serializers.validated_data['logged_by']
            username=serializers.validated_data['name']
            receiver=serializers.validated_data['email']
            serializers.save()
            
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = "Here is your requested email report:</p> <br> <ul><li>date: " + str(date) + " </li><li>transaction no.: " + str(transaction_no) + "</li><li>customer's name: " + str(customer) + " </li><li>customer's phone number: " + str(customer_no) + "</li><li>amount: " + str(amount) + "</li><li>amount transferred to bank: " + str(to_bank) + "</li><li>daily total: " + str(total_td) + "</li><li>cumulative amount: " + str(cumulative_amount) + "</li><li>logged by: " + str(logged_by) + "</li></ul> <br> <small> The data committee, <br> LogOnGo. <br> ©Pebo Kenya Ltd  </small>"
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

@permission_classes([IsAuthenticated,])
class EmailCreditCardReport(APIView):
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
            card_no=serializers.validated_data['card_no']
            amount=serializers.validated_data['amount']
            total_td=serializers.validated_data['total_td']
            cumulative_amount=serializers.validated_data['cumulative_amount']
            
            logged_by=serializers.validated_data['logged_by']
            username=serializers.validated_data['name']
            receiver=serializers.validated_data['email']
            serializers.save()
            
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = "Here is your requested email report:</p> <br> <ul><li>date: " + str(date) + " </li><li>card name.: " + str(card_name) + "</li><li>card number: " + str(card_no) + " </li><li>amount: " + str(amount) + "</li><li>daily total: " + str(total_td) + "</li><li>cumulative amount: " + str(cumulative_amount) + "</li><li>logged by: " + str(logged_by) + "</li></ul> <br> <small> The data committee, <br> LogOnGo. <br> ©Pebo Kenya Ltd  </small>"
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

@permission_classes([IsAuthenticated,])
class IncidentReport(APIView):
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
            username=serializers.validated_data['name']
            incident_date=serializers.validated_data['date']
            # date_and_time_reported=serializers.validated_data['date_and_time_reported']
            sender=serializers.validated_data['email']
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

@permission_classes([IsAdminUser,])
class IncidentDetails(APIView):
    def get(self, request, id, format=None):
        contact = Incident.objects.all().filter(pk=id).last()
        serializers = IncidentSerializer(contact,many=False)
        return Response(serializers.data)

    def delete(self, request, id, format=None):
        contact = Incident.objects.all().filter(pk=id).last()
        contact.delete()
        return Response(status=status.HTTP_200_OK) 

@permission_classes([IsAuthenticated,])
class ContactAdmin(APIView):
    
    def get(self, request, format=None):
        reports = Contact.objects.all()
        serializers = ContactSerializer(reports,many=True)
        return Response(serializers.data)

    
    def post(self, request,format=None):
        serializers = ContactSerializer(data=request.data)
        if serializers.is_valid():
            serializers.is_valid(raise_exception=True)
            date=serializers.validated_data['date']
            contact_subject=serializers.validated_data['subject']
            contact_message=serializers.validated_data['message']
            name=serializers.validated_data['name']
            sender=serializers.validated_data['email']
            # date_and_time_reported=serializers.validated_data['date_and_time_reported']
            
            serializers.save()
            receiver='fullstack.benie@gmail.com'
            admin='Janja'
            
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = "You have received a message on LogOnGo from " + str(name) + " of the email: " + str(sender) + ". Here is the message::</p> <br> <p>" + str(contact_message) + "</p> <br> <small> The contact team, <br> LogOnGo. <br> ©Pebo Kenya Ltd  </small>"
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
    
@permission_classes([IsAdminUser,])
class ContactDetails(APIView):
    def get(self, request, id, format=None):
        contact = Contact.objects.all().filter(pk=id).last()
        serializers = ContactSerializer(contact,many=False)
        return Response(serializers.data)
    
    def delete(self, request, id, format=None):
        contact = Contact.objects.all().filter(pk=id).last()
        contact.delete()
        return Response(status=status.HTTP_200_OK) 

@permission_classes([IsAuthenticated,])
class DeleteLogRequest(APIView):
    def post(self, request):
        serializer = DeleteLogRequestSerializer(data=request.data)
        if serializer.is_valid():
            log_id = request.data['log_id']
            date = request.data['date']
            date_requested = request.data['date_requested']
            logged_by = request.data['logged_by']
            receiver='fullstack.benie@gmail.com'
            username='Janja'
            user = request.data['user']
            serializer.save()
            myHtml = render_to_string('email/delete-log-request.html', {
                'log_id':log_id,
                'date':date,
                'date_requested':date_requested,
                'username':username,
                'logged_by':logged_by,
                'user':user,
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

@permission_classes([IsAuthenticated,])
class DeleteMpesaRequest(APIView):
    def post(self, request):
        serializer = DeleteMpesaRequestSerializer(data=request.data)
        if serializer.is_valid():
            log_id = request.data['log_id']
            date = request.data['date']
            date_requested = request.data['date_requested']
            logged_by = request.data['logged_by']
            user = request.data['user']
            serializer.save()
            receiver='fullstack.benie@gmail.com'
            username='Janja'
            myHtml = render_to_string('email/delete-mpesa-request.html', {
                'log_id':log_id,
                'date':date,
                'date_requested':date_requested,
                'username':username,
                'logged_by':logged_by,
                'user':user,
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

@permission_classes([IsAuthenticated,])
class DeleteCreditCardRequest(APIView):
    def post(self, request):
        serializer = DeleteCreditRequestSerializer(data=request.data)
        if serializer.is_valid():
            log_id = request.data['log_id']
            date = request.data['date']
            date_requested = request.data['date_requested']
            logged_by = request.data['logged_by']
            user = request.data['user']
            serializer.save()
            receiver='fullstack.benie@gmail.com'
            username='Janja'
            myHtml = render_to_string('email/delete-credit-request.html', {
                'log_id':log_id,
                'date':date,
                'date_requested':date_requested,
                'username':username,
                'logged_by':logged_by,
                'user':user,
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

@permission_classes([IsAdminUser,])
class LogSummary(APIView):
    def get(self,request):
        today = dt.date.today()
        log = Log.objects.all().filter(date=today)
        last = log.last()
        if last:
            last.amount_td = log.aggregate(TOTAL = Sum('amount_td'))['TOTAL']
            last.save()
            last.refresh_from_db()
            serializers = ContactSerializer(log,many=False)
            return Response(serializers.data)
        return Response(status.HTTP_204_NO_CONTENT)

@permission_classes([IsAdminUser,])
class CardSummary(APIView):
    
    def get(self,request):
        today = dt.date.today()
        log = LogCreditCard.objects.all().filter(date=today)
        last = log.last()
        if last:
            last.amount = log.aggregate(TOTAL = Sum('amount'))['TOTAL']
            last.save()
            last.refresh_from_db()
            serializers = ContactSerializer(log,many=False)
            return Response(serializers.data)
        return Response(status.HTTP_204_NO_CONTENT)

@permission_classes([IsAdminUser,])
class MpesaSummary(APIView):
    def get(self,request):
        today = dt.date.today()
        log = LogMpesa.objects.all().filter(date=today)
        last = log.last()
        if last:
            last.amount = log.aggregate(TOTAL = Sum('amount_td'))['TOTAL']
            last.save()
            last.refresh_from_db()
            serializers = ContactSerializer(log,many=False)
            return Response(serializers.data)
        return Response(status.HTTP_204_NO_CONTENT)
