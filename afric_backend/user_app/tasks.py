# auth_app/tasks.py
from celery import shared_task
from twilio.rest import Client
from django.conf import settings
from .models import User
from twilio.rest import Client


@shared_task
def send_otp(phone,otp):
    print("Task calllllllled !")
    #user = User.objects.get(phone=phone)
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        to=phone,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=f"Your OTP code is {otp}",
    )
    print(f"Sent ---------> :{otp}")

    return message.sid
