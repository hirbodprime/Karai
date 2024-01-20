from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import get_object_or_404

from accounts.models import CustomUser
from .serializers import SignupSerializer,LoginSerializer,CodeVerificationSerializer, ResendCodeSerializer
from accounts.send_sms import send_sms_code

import random

class ResendCodeView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            verification_code = str(random.randint(10000,99999))  # Implement this function
            user.sms_verification_code = verification_code
            user.save()
            # send_sms(phone_number, verification_code)  # Send SMS
            return Response({"message": "Verification code resent."})
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate and send verification code
            verification_code = str(random.randint(10000,99999))  # Implement this function
            user.sms_verification_code = verification_code
            user.save()
            # send_sms_code(user.phone_number, verification_code)  # Send SMS
            return Response({'message':f'Verification code sent to {user.phone_number}'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        verification_code = request.data.get('verification_code')
        user = get_object_or_404(CustomUser,phone_number=phone_number)
        if user.sms_verification_code == verification_code:
        # if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class CodeVerificationView(APIView):
    def post(self, request):
        serializer = CodeVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            sms_verification_code = serializer.validated_data['sms_verification_code']

            try:
                user = CustomUser.objects.get(phone_number=phone_number, sms_verification_code=sms_verification_code)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Invalid phone number or verification code'}, status=400)

            # Verify the phone number
            user.is_phone_verified = True
            user.sms_verification_code = None  # Clear the code after successful verification
            user.save()
            refresh = RefreshToken.for_user(request.user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({'message': 'Phone number verified successfully', "access_token":access_token, "refresh_token":refresh_token})

        return Response(serializer.errors)
