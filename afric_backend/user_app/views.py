# auth_app/views.py
import json
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from user_app.models import *
from .tasks import *
from django.contrib.auth import login



from django.contrib.auth import authenticate, login, get_user
from django.shortcuts import render

@csrf_exempt
@api_view(['POST'])
def login_view(request):
    print("Logging in ...")
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        user = authenticate(request, phone=phone, password=password)
        if user is not None:
            login(request, user)
            # Rediriger l'utilisateur vers une page de succès ou autre
            print("Connected !!!")
        else:
            # Afficher un message d'erreur indiquant que l'authentification a échoué
            return JsonResponse({'error_message': 'Invalid phone number or password'})
    return JsonResponse({'success': True, 'message': 'Connected Succesfully'})

@csrf_exempt
@api_view(['POST'])
def send_otp_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        print(password)
        otp = f"{random.randint(100000, 999999)}"
        request.session['otp'] = otp
        
        request.session['otp_created_at'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        send_otp(phone,otp=otp)

        print(request.session.keys())
        return JsonResponse({'success': True, 'message': 'OTP sent successfully'})

from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

@csrf_exempt
def verify_otp_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        otp = request.POST.get('otp')
        password = request.POST.get('password')
        
        cookies = request.COOKIES
     

        
        if 'sessionid' in cookies:
            session_key = cookies['sessionid']
            try:
                print("ll")
                session = Session.objects.get(session_key=session_key)
                print("22")
                session_data = session.get_decoded()
                print("33")
                
                if 'otp' in session_data and 'otp_created_at' in session_data:
                    if otp == session_data['otp']:
                        
                        otp_created_at_str = session_data['otp_created_at']
                        #otp_created_at = timezone.make_aware(timezone.datetime.strptime(otp_created_at_str, '%Y-%m-%d %H:%M:%S'))
                        otp_created_at = timezone.make_aware(timezone.datetime.strptime(otp_created_at_str, '%Y-%m-%d %H:%M:%S'))
                        if otp_created_at and timezone.now() <= otp_created_at + timezone.timedelta(minutes=10):
                            print(f"Le OTP --> {session_data['otp']}")
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


# @csrf_exempt
# @api_view(['POST'])
# def faire_un_pret(request):
#     if request.method == 'POST':
#         montant = request.POST.get('montant')
#         id = request.POST.get('user')
        
#         # user = get_user(id)
#         # if user is not None:
#         #     print(user)
#         # else:
#         #     print("no user found")
#         #     return JsonResponse({"message":"user not found"})
#         print("voici le user id")
#         print(id)
#         print("voici le montant")
#         print(montant)
#         pret = Pret(montant=montant, user=id)
#         print(pret + "voici l'objet pret")
#         pret.save()
#         print(pret.taux_interet)
#         print(pret.encours)
#         return JsonResponse({"success":True, "message":"Pret effectuer aevc succcess"})
#     return JsonResponse({"success":False, "message":"Une erreur est survenue"})
 
@csrf_exempt
@api_view(['POST'])
def faire_un_pret(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        montant = data.get('montant')
        user_id = data.get('user')
        
        try:
            # Fetch the User instance
            print(user_id)
            print(montant)
            user = User.objects.get(id=user_id)
            print("this is the user object"+user.phone)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "message": "User not found"})
        total_encours = 0
        anciens_prets = Pret.objects.filter(user=user)
        for ancien_pret in anciens_prets:
            total_encours = total_encours + ancien_pret.encours
        
        print("voicis le total encours"+str(total_encours))
        # Create the Pret instance
        if total_encours == 0:
            pret = Pret(montant=montant, user=user)
            print("innnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
            pret.save()
            print(pret.delais)
        
            return JsonResponse({"success": True, "message": "Pret effectuer avec succès"})
        elif total_encours > 0:
            return JsonResponse({"success": False, "message": "Vous devez payer tout les encours pour pouvoir effectuer un nouveau pret"})
    
    return JsonResponse({"success": False, "message": "Une erreur est survenue"})

@csrf_exempt
@api_view(['PUT'])
def faire_remboursement(request, pk):
    if request.method == 'PUT':
        a_payer = request.data.get('solde_payer')
        
        try:
            # Fetch the Pret instance by primary key (id)
            pret = Pret.objects.get(id=pk)
            print("this is the pret object: " + str(pret.id))
        except Pret.DoesNotExist:
            return JsonResponse({"success": False, "message": "Erreur de l'obtention de l'objet Pret"})
        if pret.encours == 0:
            return JsonResponse({"success": False, "message": "Rien a rembourser"})
        print("Solde a payer: " + str(a_payer))
        pret.solde_payer = a_payer
        pret.save()
        print("Montant total: " + str(pret.montant))
        print("Encours: " + str(pret.encours))
        return JsonResponse({"success": True, "message": "Remboursement effectuer avec succès"})
    
    return JsonResponse({"success": False, "message": "Une erreur lors du remboursement"})

@csrf_exempt
@api_view(['GET'])
def get_prets_by_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "Utilisateur non trouvé"})

    prets = Pret.objects.filter(user=user)
    prets_data = [
        {
            "id": pret.id,
            "user":user_id,
            "rembourser":pret.rembourser,
            "montant": pret.montant,
            "taux_interet": pret.taux_interet,
            "encours": pret.encours,
            "delais":pret.delais,
            "solde_total":pret.solde_total,
            "solde_payer": pret.solde_payer,
        }
        for pret in prets
    ]
    
    return JsonResponse({"success": True, "prets": prets_data})