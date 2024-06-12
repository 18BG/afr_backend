# auth_app/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('send_otp/', send_otp_view, name='send_otp'),
    path('verify_otp/', verify_otp_view, name='verify_otp'),
    path('login/', login_view, name='login'),
    #path('get_csrf/', get_csrf_token, name='get_csrf'),
    #path('verify_otp/', PhoneOTPView.as_view(), name="verify_otp")

]
