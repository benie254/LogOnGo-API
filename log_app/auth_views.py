from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from log_app.email import send_welcome_email
from log_app.renderers import UserJSONRenderer
from log_app.models import MyUser
from log_app.auth_serializer import UserSerializer
import jwt, datetime
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from django.core.mail import send_mail
from django.http import Http404
import os
import sendgrid
from sendgrid.helpers.mail import *
from decouple import config 

# Create your views here.
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
        serializer.save()
        sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
        from_email = Email("davinci.monalissa@gmail.com")
        to_email = To(receiver)
        subject = "Sending with SendGrid is Fun"
        content = Content("text/plain", "and easy to do anywhere, even with Python")
        mail = Mail(from_email, to_email, subject, content)

        mail_json = mail.get()

        response = sg.client.mail.send.post(request_body=mail_json)
        print(response.status_code)
        print(response.headers)
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