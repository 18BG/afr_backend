# auth_app/views.py
import secrets
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from user_app.models import *
from .tasks import *
from django.contrib.auth import login



from django.contrib.auth import authenticate, login
from django.shortcuts import render

@csrf_exempt
@api_view(['POST'])
def login_view(request):
    print("Logging in ...")
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        print(f"Mot de passe et numero ==== {password} -- {phone}")
        
        user = authenticate(request, phone=phone, password=password)
        print(f"L'utilisateur ==== {user}")
        if user is not None:
            us = User.objects.get(phone=phone)
            print(us.id)
            login(request, user)
            # Rediriger l'utilisateur vers une page de succès ou autre
            print("Connected !!!")
        else:
            # Afficher un message d'erreur indiquant que l'authentification a échoué
            return JsonResponse({'success':False,'error_message': 'Numéro de téléphone ou mot de passe invalide'})
    return JsonResponse({'success': True, 'message': 'Connected Succesfully','phone':phone,'password':password,'id':us.id})

@csrf_exempt
@api_view(['POST'])
def send_otp_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        print(password)
        #otp = f"{random.randint(100000, 999999)}"
        otp = f"{secrets.randbelow(9000) + 1000}"
        request.session['otp'] = otp
        request.session['otp_created_at'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        send_otp(phone,otp=otp)

        print(request.session.keys())
        return JsonResponse({'success': True, 'message': 'OTP sent successfully'})

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

@csrf_exempt
def verify_otp_view(request):
   # import pdb; pdb.set_trace()
    if request.method == 'POST':
        phone = request.POST.get('phone')
        phone = request.POST.get('phone')
        otp = request.POST.get('otp')
        password = request.POST.get('password')
        print(f"Mot de passe in verify-- {password}")
        print(f"Otp in verify-- {password}")
        print(f"phone in verify-- {password}")
        cookies = request.COOKIES
     

        
        if 'sessionid' in cookies:
            session_key = cookies['sessionid']
            try:
                session = Session.objects.get(session_key=session_key)
                session_data = session.get_decoded()
                
                if 'otp' in session_data and 'otp_created_at' in session_data:
                    if otp == session_data['otp']:
                        
                        otp_created_at_str = session_data['otp_created_at']
                        #otp_created_at = timezone.make_aware(timezone.datetime.strptime(otp_created_at_str, '%Y-%m-%d %H:%M:%S'))
                        otp_created_at = timezone.make_aware(timezone.datetime.strptime(otp_created_at_str, '%Y-%m-%d %H:%M:%S'))
                        if otp_created_at and timezone.now() <= otp_created_at + timezone.timedelta(minutes=10):
                            print(f"Le OTP --> {session_data['otp']}")
                                    # Vérification de l'unicité du numéro de téléphone
                            existing_user = User.objects.filter(phone=phone).first()
                            if existing_user:
                                #login(request, user)
                                # Un utilisateur avec le même numéro de téléphone existe déjà
                                return JsonResponse({'success': False, 'message': 'Un compte avec ce numéro de téléphone existe déjà.'}, status=400)
                            user ,created= User.objects.get_or_create(phone=phone,password=password)
                            if created:
                                
                                user.set_password(password)
                                user.save()
                            print(f"les cookies : {cookies}")
                            # OTP is valid, connect the user
                            #user.backend = 'django.contrib.auth.backends.ModelBackend'  # Set user backend
                            login(request, user)  # Log in the user
                            print(f"Creation date --> {session_data['otp_created_at']}")
                            return JsonResponse({'success': True, 'message': 'OTP verified successfully'})
            except Session.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Session does not exist'}, status=400)
        # Invalid OTP or OTP expired
        return JsonResponse({'success': False, 'message': 'Invalid OTP'}, status=400)
    
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)







