from django.contrib.auth.backends import BaseBackend
from .models import CustomUser

class PhoneAuthBackend(BaseBackend):
    def authenticate(self, request, phone_number=None, sms_code=None):
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            if user.sms_verification_code == sms_code and user.is_phone_verified:
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
