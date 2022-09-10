from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import render_to_string
import sendgrid
from sendgrid.helpers.mail import *
from decouple import config 


def send_welcome_email(username,to_email):
    sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
    from_email = 'logongo.ke@gmail.com'
    subject = "You're in!"

    text_content = render_to_string('email/welcome.txt',{"username":username})
    html_content = render_to_string('email/welcome.html',{"username":username,})

    msg = EmailMultiAlternatives(subject,text_content,from_email,[to_email])
    content = msg.attach_alternative(html_content,'text/html')
    # msg.send() 
    mail = Mail(from_email, to_email, subject, content)

    mail_json = mail.get()

    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)
