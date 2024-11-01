"""
This module defines the URL patterns for the 'accounts' application.

It maps specific URLs to the corresponding views that handle requests for Spotify authentication.

URL Patterns:
    - 'get-auth-url': Maps to the `AuthURL` view, which provides the Spotify authorization URL.
    - 'redirect': Maps to the `spotify_callback` view, which handles the Spotify redirect 
                    after authentication.
    - 'is-authenticated': Maps to the `IsAuthenticated` view, which checks if the user is 
                            authenticated with Spotify.

Usage:
    Add these URL patterns to the main `urls.py` file of the project to include
    Spotify authentication functionality for the 'accounts' app.
"""
from django.urls import path
from .views import AuthURL, spotify_callback, IsAuthenticated

# URL patterns for handling Spotify authentication.
urlpatterns = [
    path('get-auth-url', AuthURL.as_view(), name='auth-url'),
    path('callback', spotify_callback, name='spotify-callback'),
    path('is-authenticated', IsAuthenticated.as_view(), name='is-authenticated')
]
