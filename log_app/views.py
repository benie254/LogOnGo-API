from django.shortcuts import get_object_or_404, render,redirect

from log_app.models import Fuel, Log, LogMpesa, MyUser 

def home(request):
    fuels = Fuel.objects.all()
    users = MyUser.objects.all()
    logs = Log.objects.all()
    mpesa = LogMpesa.objects.all()
    print(fuels)
    return render(request,'index.html',{"fuels":fuels,"users":users,"logs":logs})