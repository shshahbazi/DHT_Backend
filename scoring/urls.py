from django.urls import path

from scoring.views import FeatureListApiView, FeatureDetailApiView, PurchaseFeatureApiView

urlpatterns = [
    path('feature/list/', FeatureListApiView.as_view(), name='features-list'),
    path('feature/<int:pk>/', FeatureDetailApiView.as_view(), name='feature-detail'),
    path('feature/purchase/<int:pk>/', PurchaseFeatureApiView.as_view(), name='purchase-feature')

]
