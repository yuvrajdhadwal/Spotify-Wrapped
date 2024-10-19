from django.urls import path
from .views import AuthURL, spotify_callback, IsAuthenticated

# Create your views here.

urlpatterns = [
    path('get-auth-url', AuthURL.as_view(), name='auth-url'),
    path('redirect', spotify_callback),
    path('is-authenticated', IsAuthenticated.as_view())
]