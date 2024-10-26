"""
This file is used to define the URL patterns for the Spotify Data API endpoint
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SongViewSet

router = DefaultRouter()
router.register(r'songs', SongViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
