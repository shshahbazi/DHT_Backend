from django.urls import path

from user.views import AuthLoginUser, VerifyOTPLogin, LogOutApi

urlpatterns = [
    path('login/', AuthLoginUser.as_view(), name='login'),
    path('login/verify-otp/', VerifyOTPLogin.as_view(), name='verify-otp'),
    path('logout/', LogOutApi.as_view(), name='logout')
]