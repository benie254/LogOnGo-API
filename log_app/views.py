from django.shortcuts import get_object_or_404, render,redirect

from log_app.models import Announcement, Fuel, Log, LogMpesa, MyUser, Profile 
import datetime as dt 
from django.core.paginator import Paginator

def home(request):
    fuels = Fuel.objects.all()
    users = MyUser.objects.all()
    logs = Log.objects.all()
    paginator = Paginator(logs,5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    mpesa = LogMpesa.objects.all()
    today = dt.date.today()
    prof = Profile.objects.all().last()
    announcements = Announcement.objects.all()
    today_fuel_log = Log.objects.all().filter(date=today).filter(fuel_id=1).first()
    # petrol_received = FuelReceived.objects.all().filter(fuel_id=1).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
    print(fuels)
    return render(request,'index.html',{"fuels":fuels,"users":users,"logs":logs,"today_fuel_log":today_fuel_log,"prof":prof,"announcements":announcements,"page_obj":page_obj})