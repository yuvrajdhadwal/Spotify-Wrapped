from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
import os
from dotenv import load_dotenv
from requests import post

"""
Gets the user's tokens from the database. Database stores everything based on user which is the
session id.
"""
def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None

"""
Given session id, checks if the user is already in the database, if not, then create that user
if they are and their token as expired, refresh their token and update their row in the database
"""
def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(session_id=session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.token_type = token_type
        tokens.expires_in = expires_in
        tokens.refresh_token = refresh_token
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = SpotifyToken(user=session_id, access_token=access_token, token_type=token_type,
                              expires_in=expires_in, refresh_token=refresh_token)
        tokens.save()

"""
Checks whether a user is authenticated
To do this, first we check if that user is in our database, if they are but their token is expired
refresh their token and return true because we just authenticated them
if their token is not expired then send true too
if they have never created an account in the database, return false
"""
def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id=session_id)

        return True
    return False

"""
Refreshes the spotify token by making an api request to spotify then updates the user in the database
"""
def refresh_spotify_token(session_id):
    load_dotenv()
    refresh_token = get_user_tokens(session_id=session_id).refresh_token

    response = post('https://accounts.spotify.com/api/tokens', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET')
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    
    update_or_create_user_tokens(session_id=session_id, access_token=access_token, token_type=token_type,
                                 refresh_token=refresh_token, expires_in=expires_in)