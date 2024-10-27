"""
Utils used in spotify_data/views.
"""

import requests

def get_spotify_user_data(access_token):
    """
    Retrieves current user data including spotify id, email, profile image, and username.

    Parameters:
        - access_token: the access token associated with the current session

    Returns:
        JSON response containing user data
    """

    # Fetch the user's data from Spotify API
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.get('https://api.spotify.com/v1/me', headers=headers, timeout=5)
    return response.json() if response.status_code == 200 else None

def get_user_favorite_tracks(access_token, timelimit):
    """
    Returns a list of 20 user favorite tracks over one of three time periods:
    - short-term: 4 weeks
    - medium-term: 6 months
    - long-term: 1 year

    Parameters:
        - access_token: the access token associated with the current session
        - timelimit: the desired term

    Returns:
        JSON response containing user favorite tracks
    """

    # Fetch the user's data from Spotify API
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    params = {
        'time_limit': timelimit,
        'limit': 20
    }
    response = requests.get('https://api.spotify.com/v1/me/top/tracks',
                            headers=headers, params=params, timeout=5)
    return response.json() if response.status_code == 200 else None

def get_user_favorite_artists(access_token, timelimit):
    """
    Returns a list of 20 user favorite artists over one of three time periods:
    - short-term: 4 weeks
    - medium-term: 6 months
    - long-term: 1 year

    Parameters:
        - access_token: the access token associated with the current session
        - timelimit: the desired term

    Returns:
        JSON response containing user favorite artists
    """

    # Fetch the user's data from Spotify API
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    params = {
        'time_limit': timelimit,
        'limit': 20
    }
    response = requests.get('https://api.spotify.com/v1/me/top/artists',
                            headers=headers, params=params, timeout=5)
    return response.json() if response.status_code == 200 else None
