"""
This module defines the URL patterns for the 'accounts' application.

It maps specific URLs to the corresponding views that handle requests for Spotify authentication 
and user account management, such as login, logout, and registration.

URL Patterns:
    - 'get-auth-url': Maps to the `AuthURL` view, which provides the Spotify authorization URL.
    - 'callback': Maps to the `spotify_callback` view, which handles the Spotify redirect 
                  after authentication.
    - 'is-authenticated': Maps to the `IsAuthenticated` view, which checks if the user is 
                          authenticated with Spotify.
    - 'login': Maps to the `sign_in` view, which handles user login.
    - 'logout': Maps to the `sign_out` view, which handles user logout.
    - 'register': Maps to the `sign_up` view, which handles user registration.
    - 'get-csrf-token': Maps to the `get_csrf_token` view, which provides
        a CSRF token for the frontend.

Usage:
    Add these URL patterns to the main `urls.py` file of the project to enable Spotify 
    authentication and account management functionality for the 'accounts' app.
"""
from django.urls import path
from .views import AuthURL, spotify_callback, IsAuthenticated, sign_in, sign_out
from .views import sign_up, get_csrf_token

# URL patterns for handling Spotify authentication.
urlpatterns = [
    path('get-auth-url/', AuthURL.as_view(), name='auth-url'),
    path('callback/', spotify_callback, name='spotify-callback'),
    path('is-authenticated/', IsAuthenticated.as_view(), name='is-authenticated'),
    path("login/", sign_in, name="login"),
    path("logout/", sign_out, name="logout"),
    path("register/", sign_up, name='register'),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
]
