from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from log_app.email import send_welcome_email
from log_app.renderers import UserJSONRenderer
from log_app.models import MyUser, Site, Profile
from log_app.auth_serializer import PetrolStationSerializer, UserProfileSerializer, UserSerializer
import jwt, datetime
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from django.core.mail import send_mail
from django.http import Http404
import os
import sendgrid
from sendgrid.helpers.mail import *
from decouple import config 

# Create your views here.'
class UserProfile(APIView):
    def get_user_profiles(self,request):
        try:
            user_id = request.user.id
            return Profile.objects.all().filter(id=user_id)
        except Profile.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        user_id = request.user.id
        profiles = Profile.objects.all().filter(id=user_id)
        serializers = UserProfileSerializer(profiles,many=False)

        return Response(serializers.data)
class AllProfiles(APIView):
    def get_all_profiles(self):
        try:
            return Profile.objects.all()
        except Profile.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializers = UserProfileSerializer(profiles,many=True)
        return Response(serializers.data)

class AllUserStations(APIView):
    def get_all_profiles(self):
        try:
            return Site.objects.all()
        except Site.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        stations = Site.objects.all()
        serializers = PetrolStationSerializer(stations,many=True)
        return Response(serializers.data)

class UserProfiles(APIView):
    def get_all_users(self):
        try:
            return MyUser.objects.all()
        except MyUser.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        user_profiles = MyUser.objects.all()
        serializers = UserSerializer(user_profiles,many=True)
        return Response(serializers.data)

class RegisterView(APIView):
    # renderer_classes = (UserJSONRenderer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username=serializer.validated_data['username']
        receiver=serializer.validated_data['email']
        user = serializer.save()
        user.refresh_from_db()
        user.profile.first_name = serializer.validated_data['first_name']
        user.profile.last_name = serializer.validated_data['last_name']
        user.profile.username = serializer.validated_data['username']
        user.profile.email = serializer.validated_data['email']
        user.site.petrol_station = serializer.validated_data['petrol_station']
            # user.is_active = False
        user.save()
        sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
        msg = "Nice to have you on board LogOnGo. Let's get to work!</p> <br> <small> The welcome committee, <br> LogOnGo. <br> ©Pebo Kenya Ltd  </small>"
        message = Mail(
            from_email = Email("davinci.monalissa@gmail.com"),
            to_emails = receiver,
            subject = "You're in!",
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
        # content = Content("text/plain", "and easy to do anywhere, even with Python")
        # mail = Mail(from_email, subject, content,to_emails)

        # mail_json = mail.get()

        # response = sg.client.mail.send.post(request_body=mail_json)
        # print(response.status_code)
        # print(response.headers)
        # send_welcome_email(username,receiver)
        return Response(serializer.data)


class LoginView(APIView):
    # renderer_classes = (UserJSONRenderer)
    def post(self, request):
        email = request.data['email']
        employee_id = request.data['employee_id']
        password = request.data['password']

        user = MyUser.objects.filter(email=email,employee_id=employee_id).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class UserView(APIView):
    # renderer_classes = (UserJSONRenderer)
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = MyUser.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

# class UsrProf(APIView):
#     def get_user_profiles(self):
#         try:
#             return Profile.objects.all()
#         except Profile.DoesNotExist:
#             return Http404

#     def get(self, request, format=None):
#         usr_profiles = Profile.objects.all()
#         serializers = UsrProf()
#         return Response(serializers.data)