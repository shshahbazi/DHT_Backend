"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from core import base
from user.views import GitHubLogin

schema_view = get_schema_view(
    openapi.Info(
        title="Doost API",
        default_version='v1',
        description="Doost API Documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('user.urls')),
    path('habits/', include('habit.urls')),
    path('github/', GitHubLogin.as_view(), name='github-login'),
    path('accounts/', include('allauth.urls')),
    path('mood-tracker/', include('mental.urls')),
    path('exercise/', include('exercise.urls')),
    path('scoring/', include('scoring.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)
