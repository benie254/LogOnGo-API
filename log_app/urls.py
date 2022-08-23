from django.conf.urls import include 
from django.urls import path,re_path as url 
from log_app import views 


urlpatterns = [
    url(r'^api/petrol-info/$', views.PetrolInfo.as_view()),
    url(r'^api/our-fuels/$', views.RegisteredFuels.as_view()),
]