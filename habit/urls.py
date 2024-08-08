from django.urls import path

from habit.views import WorkSessionStartApi, WorkSessionEndApi, EndHabitInstanceApi

urlpatterns = [
    path('start-work/', WorkSessionStartApi.as_view(), name='start_work'),
    path('end-work/', WorkSessionEndApi.as_view(), name='end_work'),
    path('end-habit/<int:habit_instance_id>/', EndHabitInstanceApi.as_view(), name='end_habit')
]