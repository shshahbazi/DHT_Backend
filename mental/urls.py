from django.urls import path

from mental.views import SubmitMood

urlpatterns = [
    path('submit/', SubmitMood.as_view(), name='submit-daily-mood')
]