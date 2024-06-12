#from rest_framework import serializers

#from user_app.models import PhoneOTP
# from django.contrib.auth import get_user_model,authenticate
# from .models import OTP

# User = get_user_model()

# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('email', 'phone_number', 'password')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user

# class OTPSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OTP
#         fields = '__all__' #('phone_number',)

# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=False)
#     phone_number = serializers.CharField(required=False)
#     password = serializers.CharField(write_only=True, required=False)
#     otp = serializers.CharField(write_only=True, required=False)

#     def validate(self, data):
#         email = data.get('email')
#         phone_number = data.get('phone_number')
#         password = data.get('password')
#         otp = data.get('otp')

#         if email:
#             user = authenticate(email=email, password=password)
#         elif phone_number:
#             otp_instance = OTP.objects.filter(user__phone_number=phone_number, otp=otp).first()
#             if otp_instance and otp_instance.is_valid():
#                 user = otp_instance.user
#             else:
#                 raise serializers.ValidationError('Invalid OTP.')
#         else:
#             raise serializers.ValidationError('Must include "email" or "phone_number".')

#         if user and user.is_active:
#             return user
#         raise serializers.ValidationError('Unable to log in with provided credentials.')




# class PhoneOTPSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PhoneOTP
#         fields = ['phone_number']