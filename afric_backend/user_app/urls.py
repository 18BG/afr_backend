# auth_app/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('send_otp/', send_otp_view, name='send_otp'),
    path('verify_otp/', verify_otp_view, name='verify_otp'),
    path('login/', login_view, name='login'),
    path('pret/', faire_un_pret, name='pret'),
    path('remboursement/<int:pk>/', faire_remboursement, name='rembourser'),
    path('user/<int:user_id>/prets/', get_prets_by_user, name='get_prets_by_user'),
    #path('get_csrf/', get_csrf_token, name='get_csrf'),
    #path('verify_otp/', PhoneOTPView.as_view(), name="verify_otp")

]
