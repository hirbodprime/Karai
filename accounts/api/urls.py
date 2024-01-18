from django.urls import path
from .views import SignupView, LoginView,CodeVerificationView, ResendCodeView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify-code/', CodeVerificationView.as_view(), name='verify_code'),
    path('login/', LoginView.as_view(), name='login'),

    path('resend-code/', ResendCodeView.as_view(), name='resend_code'),

]
