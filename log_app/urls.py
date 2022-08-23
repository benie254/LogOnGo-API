from django.conf.urls import include 
from django.urls import path,re_path as url 
from log_app import api_views 


urlpatterns = [
    url(r'^api/petrol-info/$', api_views.PetrolInfo.as_view()),
    url(r'^api/our-fuels/$', api_views.RegisteredFuels.as_view()),
]