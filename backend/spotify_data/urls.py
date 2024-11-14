"""
This file is used to define the URL patterns for the Spotify Data API endpoint
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SongViewSet, update_or_add_spotify_user, add_spotify_wrapped, add_duo_wrapped

router = DefaultRouter()
router.register(r'songs', SongViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('updateuser', update_or_add_spotify_user,
         name='update_or_add_spotify_user'),
    path('addwrapped/<str:term_selection>', add_spotify_wrapped, name='add_spotify_wrapped'),
    path('addduo/<str:term_selection>/<str:user2>', add_duo_wrapped, name='add_duo_wrapped')
]
