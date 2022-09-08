from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import render_to_string

def send_welcome_email(username,receiver):
    subject = "You're in!"
    sender = 'davinci.monalissa@gmail.com'

    text_content = render_to_string('email/welcome.txt',{"username":username})
    html_content = render_to_string('email/welcome.html',{"username":username,})

    msg = EmailMultiAlternatives(subject,text_content,sender,[receiver])
    msg.attach_alternative(html_content,'text/html')
    msg.send()