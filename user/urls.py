from django.urls import path

from user.views import AuthLoginUser, UserRegistrationView

urlpatterns = [
    path('login/', AuthLoginUser.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register-user')
]