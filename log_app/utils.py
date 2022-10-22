# from calendar import timegm
# from datetime import datetime
# from rest_framework_jwt.compat import get_username, get_username_field
# from rest_framework_jwt.settings import api_settings
# from django_otp.models import Device
# def jwt_otp_payload(user, device = None):
#     """
#     Optionally include OTP device in JWT payload
#     """
#     username_field = get_username_field()
#     username = get_username(user)
        
#     payload = {
#         'user_id': user.pk,
#         'username': username,
#         'first_name':user.first_name,
#         'last_name':user.last_name,
#         'petrol_station':user.petrol_station,
#         'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
#     }
        
#     # Include original issued at time for a brand new token,
#     # to allow token refresh
#     if api_settings.JWT_ALLOW_REFRESH:
#         payload['orig_iat'] = timegm(
#             datetime.utcnow().utctimetuple()
#         )
#     if api_settings.JWT_AUDIENCE is not None:
#         payload['aud'] = api_settings.JWT_AUDIENCE
#     if api_settings.JWT_ISSUER is not None:
#         payload['iss'] = api_settings.JWT_ISSUER
#     # custom additions
#     if (user is not None) and (device is not None) and (device.user_id == user.id) and (device.confirmed is True):
#         payload['otp_device_id'] = device.persistent_id
#     else:
#         payload['otp_device_id'] = None
#     return payload

# def get_custom_jwt(user, device):
#     """
#     Helper to generate a JWT for a validated OTP device.
#     This resets the orig_iat timestamp, as we've re-validated the user.
#     """
#     jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#     payload = jwt_otp_payload(user, device)
#     return jwt_encode_handler(payload)

from django.core.mail import EmailMessage


import threading


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        EmailThread(email).start()