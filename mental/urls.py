from django.urls import path

from mental.views import SubmitMood, MoodDistributionApiView

urlpatterns = [
    path('submit/', SubmitMood.as_view(), name='submit-daily-mood'),
    path('report/', MoodDistributionApiView.as_view(), name='report-mood')
]