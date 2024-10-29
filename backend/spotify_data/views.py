"""
Views to handle database management (users, songs, artists)
"""

from rest_framework import viewsets
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.utils import timezone
from accounts.models import SpotifyToken
from accounts.utils import is_spotify_authenticated, refresh_spotify_token
from .utils import (get_spotify_user_data,
                    get_user_favorite_artists, get_user_favorite_tracks)
from .models import Song
from .serializers import SongSerializer
from .models import SpotifyUser

class SongViewSet(viewsets.ModelViewSet):
    """
    For testing, API endpoint that allows songs to be viewed or edited.
    """
    queryset = Song.objects.all()
    serializer_class = SongSerializer

def update_or_add_spotify_user(request, session_id):
    """
    Adds the user's profile and favorite tracks if the user is not in the database.
    Updates the user's profile and favorite tracks if the user is in the database.

    Parameters:
        - request: the HTTP request object
        - session_id: the current session id used for login

    Returns:
        - success: Json Response indicating whether the user is added to the database
        - failure: Json Response indicating error
    """
    if not is_spotify_authenticated(session_id):
        return JsonResponse({'error': 'User not authenticated'}, status=403)

    user = request.user

    # Check for existing SpotifyToken
    try:
        token_entry = SpotifyToken.objects.get(user=session_id)
    except ObjectDoesNotExist:
        return HttpResponse("User add/update failed: missing access token", status=500)

    access_token = token_entry.access_token

    # Fetch user data from Spotify API
    user_data = get_spotify_user_data(access_token)

    if user_data:
        # Update or create the SpotifyUser
        spotify_user, created = SpotifyUser.objects.update_or_create(
            spotify_id=user_data['id'],
            defaults={
                'user': user,
                'spotify_id': user_data.get('id'),
                'display_name': user_data.get('display_name'),
                'email': user_data.get('email'),
                'profile_image_url': user_data.get('images')[0]['url']
                if user_data.get('images') else None,
                'favorite_tracks_short': get_user_favorite_tracks(access_token,'short_term'),
                'favorite_tracks_medium': get_user_favorite_tracks(access_token,'medium_term'),
                'favorite_tracks_long': get_user_favorite_tracks(access_token,'long_term'),
                'favorite_artists_short': get_user_favorite_artists(access_token,'short_term'),
                'favorite_artists_medium': get_user_favorite_artists(access_token,'medium_term'),
                'favorite_artists_long': get_user_favorite_artists(access_token,'long_term'),
            }
        )

        return JsonResponse({'spotify_user': {'id': spotify_user.spotify_id, 'created': created}})

    return JsonResponse({'error': 'Could not fetch user data from Spotify'}, status=500)
