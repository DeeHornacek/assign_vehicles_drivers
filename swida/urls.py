"""
URL configuration for swida project.
"""
from django.urls import path, include

urlpatterns = [
    path('', include("api.urls")),
]
