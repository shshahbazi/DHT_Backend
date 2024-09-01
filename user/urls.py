from django.urls import path

from user.views import AuthLoginUser, VerifyOTPLogin, LogOutApi, GetProfileDetails, UpdateProfilePicture

urlpatterns = [
    path('login/', AuthLoginUser.as_view(), name='login'),
    path('login/verify-otp/', VerifyOTPLogin.as_view(), name='verify-otp'),
    path('logout/', LogOutApi.as_view(), name='logout'),
    path('profile/', GetProfileDetails.as_view(), name='profile-detail'),
    path('profile/picture/', UpdateProfilePicture.as_view(), name='')
]