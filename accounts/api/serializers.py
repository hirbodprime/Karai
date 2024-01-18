from rest_framework import serializers
from accounts.models import CustomUser
class ResendCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

class CodeVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    sms_verification_code = serializers.CharField()

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['phone_number']

class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    sms_verification_code = serializers.CharField()
