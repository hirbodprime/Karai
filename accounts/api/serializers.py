from django.conf import settings

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


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'profile_image']

    profile_image = serializers.SerializerMethodField()

    def get_profile_image(self, obj):
        if obj.profile_image:
            return settings.SITE_DOMAIN + obj.profile_image.url
        return
