from typing import Any
from django.shortcuts import get_object_or_404, render,redirect 
from django.contrib.auth.models import User 
from django.http import Http404 

from rest_framework import status, generics 
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from log_app.auth_serializer import LoginSerializer, LogoutSerializer, UserSerializer

from log_app.auth_serializer import MyUserSerializer,UserRegSerializer
from log_app.models import MyUser

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request

from log_app.renderers import UserJSONRenderer

import jwt
from rest_framework_simplejwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER



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

class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserRegSerializer

    # def post(self, request: Request) -> Response:
    #     """Return user response after a successful registration."""
    #     user_request = request.data.get('user', {})
    #     serializer = self.serializer_class(data=user_request)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            user = self.model.get(username=serializer.data['username'])
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response(
                token,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        """Return user after login."""
        user = request.data.get('user', {})

        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request: Request, *args: dict[str, Any], **kwargs: dict[str, Any]) -> Response:
        """Return user on GET request."""
        serializer = self.serializer_class(request.user, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request: Request, *args: dict[str, Any], **kwargs: dict[str, Any]) -> Response:
        """Return updated user."""
        serializer_data = request.data.get('user', {})

        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        """Validate token and save."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)