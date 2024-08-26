from django.urls import path

from scoring.views import FeatureListApiView, FeatureDetailApiView

urlpatterns = [
    path('feature/list/', FeatureListApiView.as_view(), name='features-list'),
    path('feature/<int:pk>/', FeatureDetailApiView.as_view(), name='feature-detail')

]