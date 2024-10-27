import os
from dotenv import load_dotenv
import requests

def refresh_access_token(refresh_token):
    # Return the new access token and other related data as a dictionary.
    load_dotenv()
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    url = 'https://accounts.spotify.com/api/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, data=data, timeout=5)
    return response.json()

def get_spotify_user_data(access_token):
    # Fetch the user's data from Spotify API
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get('https://api.spotify.com/v1/me', headers=headers, timeout=5)
    return response.json() if response.status_code == 200 else None

def get_user_favorite_tracks(access_token, timelimit):
    # Fetch the user's data from Spotify API
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'time_limit': timelimit,
        'limit': 20
    }
    response = requests.get('https://api.spotify.com/v1/me/top/tracks',
                            headers=headers, params=params, timeout=5)
    return response.json() if response.status_code == 200 else None

def get_user_favorite_artists(access_token, timelimit):
    # Fetch the user's data from Spotify API
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'time_limit': timelimit,
        'limit': 20
    }
    response = requests.get('https://api.spotify.com/v1/me/top/artists',
                            headers=headers, params=params, timeout=5)
    return response.json() if response.status_code == 200 else None
