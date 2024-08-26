from django.urls import path

from exercise.views import ExerciseDetailView, ExerciseListView

urlpatterns = [
    path('<int:exercise_id>/', ExerciseDetailView.as_view(), name='exercise_detail'),
    path('list/', ExerciseListView.as_view(), name='list_exercise')
]