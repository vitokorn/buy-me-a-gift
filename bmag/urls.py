"""bmag URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

openapi_info = openapi.Info(
    title="Buy me a gift API",
    default_version="v1",
    description="Vinhood wants to create a new service for customers to add their favorite products to a wishlist, and the name of the service is BUY-ME-A-GIFT.",
)
schema_view = get_schema_view(
    openapi_info,
    patterns=[
        path("api/", include("api.urls")),
    ],
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    # Route schema_view.with_ui to serve the Swagger template.
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls", namespace="api")),
]
