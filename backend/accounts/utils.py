"""
This module provides utility functions to manage Spotify authentication tokens for users.

It includes functionality for retrieving, updating, and refreshing Spotify tokens,
allowing users to authenticate with the Spotify API.

Functions:
    - get_user_tokens: Retrieve Spotify tokens for a given user session.
    - update_or_create_user_tokens: Update or create Spotify tokens for a user in the database.
    - is_spotify_authenticated: Check if a user is authenticated with Spotify.
    - refresh_spotify_token: Refresh a user's Spotify access token using their refresh token.
"""
from datetime import timedelta
import os
from django.utils import timezone
from dotenv import load_dotenv
from requests import post
from accounts.models import SpotifyToken


def get_user_tokens(session_id):
    """
    Retrieve the Spotify token for a given user session.

    This function queries the database to retrieve the user's Spotify token based on the session ID.
    If a token exists, it returns the token; otherwise, it returns None.

    Parameters:
        session_id (str): The session ID of the user.

    Returns:
        SpotifyToken: The SpotifyToken object for the user if it exists, otherwise None.
    """
    # TODO: Are we still using session id?
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    return None

def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    """
    Update or create Spotify tokens for a user in the database.

    This function checks whether a user already has a Spotify token stored in the database.
    If the user exists, it updates their tokens; if not, it creates a new record.
    The expiration time for the token is calculated based on the current time.

    Parameters:
        session_id (str): The session ID of the user.
        access_token (str): The new Spotify access token.
        token_type (str): The type of token (usually 'Bearer').
        expires_in (int): The lifetime of the access token in seconds.
        refresh_token (str): The refresh token used to generate new access tokens.
    
    Returns:
        None
    """
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

def is_spotify_authenticated(session_id):
    """
    Check if a user is authenticated with Spotify.

    This function verifies if a user has valid Spotify tokens in the database.
    If the user's access token has expired, it automatically refreshes the token and returns True.
    If the token is valid or has been refreshed, the user is considered authenticated.
    If no tokens exist for the user, it returns False.

    Parameters:
        session_id (str): The session ID of the user.

    Returns:
        bool: True if the user is authenticated, False otherwise.
    """
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id=session_id)
        return True
    return False

def refresh_spotify_token(session_id):
    """
    Refresh the Spotify access token for a user.

    This function sends a POST request to Spotify's API to refresh the access token using
    the user's stored refresh token. It updates the user's tokens in the database with the new
    access and refresh tokens.

    Parameters:
        session_id (str): The session ID of the user.

    Returns:
        None
    """
    load_dotenv()
    refresh_token = get_user_tokens(session_id=session_id).refresh_token
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    if not client_id or not client_secret:
        raise TypeError("SET UP CLIENT ENV VARIABLES")

    response = post('https://accounts.spotify.com/api/tokens', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }, timeout=10).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')

    update_or_create_user_tokens(session_id=session_id, access_token=access_token,
                                 token_type=token_type, refresh_token=refresh_token,
                                 expires_in=expires_in)
