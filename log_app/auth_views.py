from django.shortcuts import get_object_or_404, render,redirect 
from django.contrib.auth.models import User 
from django.http import Http404 

from rest_framework import status, generics 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

from log_app.serializer import MyUserSerializer,UserRegSerializer
from log_app.models import MyUser 

class ProfileDetails(APIView): 
    authentication_classes = (TokenAuthentication)
    permission_classes = (AllowAny)
    
    def get_profile_details(self,request):
        try:
            return MyUser.objects.all().filter(pk=request.user.id) 
        except MyUser.DoesNotExist:
            return Http404
    
    def get(self, request, format=None, **kwargs):
        profile_details = MyUser.objects.all().filter(pk=request.user.id)
        serializers = MyUserSerializer(profile_details,many=False)
        return Response(serializers.data) 

class RegisterUser(generics.CreateAPIView):
    permission_classes = (AllowAny)
    serializer_class = UserRegSerializer 
    
