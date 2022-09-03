"""Log_Proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,TokenBlacklistView,)
from log_app import auth_views 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('log_app.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),

    path('register/', auth_views.RegistrationAPIView.as_view(), name='register_user'),
    path('login/', auth_views.LoginAPIView.as_view(), name='login_user'),
    path('logout/', auth_views.LogoutAPIView.as_view(), name="logout_user"),
    path('user-update/', auth_views.UserRetrieveUpdateAPIView.as_view(), name='user'),
]
