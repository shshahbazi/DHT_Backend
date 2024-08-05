from django.urls import path

from habit.views import WorkSessionStartApi, WorkSessionEndApi

urlpatterns = [
    path('start-work/', WorkSessionStartApi.as_view(), name='start_work'),
    path('end-work/', WorkSessionEndApi.as_view(), name='end_work')
]