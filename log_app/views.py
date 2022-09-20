from django.shortcuts import get_object_or_404, render,redirect

from log_app.models import Announcement, Fuel, Log, LogMpesa, MyUser, Profile 
import datetime as dt 

def home(request):
    fuels = Fuel.objects.all()
    users = MyUser.objects.all()
    logs = Log.objects.all()
    mpesa = LogMpesa.objects.all()
    today = dt.date.today()
    prof = Profile.objects.all().last()
    announcements = Announcement.objects.all()
    today_fuel_log = Log.objects.all().filter(date=today).filter(fuel_id=1).first()
    # petrol_received = FuelReceived.objects.all().filter(fuel_id=1).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
    print(fuels)
    return render(request,'index.html',{"fuels":fuels,"users":users,"logs":logs,"today_fuel_log":today_fuel_log,"prof":prof,"announcements":announcements})