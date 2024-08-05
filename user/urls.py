from django.urls import path

from user.views import AuthLoginUser, VerifyOTPLogin

urlpatterns = [
    path('login/', AuthLoginUser.as_view(), name='login'),
    path('login/verify-otp/', VerifyOTPLogin.as_view(), name='verify-otp'),
]