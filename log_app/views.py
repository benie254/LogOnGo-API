from django.shortcuts import get_object_or_404, render,redirect

from log_app.models import Fuel 

def home(request):
    fuels = Fuel.objects.all().last()
    return render(request,'index.html',{"fuels":fuels})