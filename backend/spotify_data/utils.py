"""
Utils used in spotify_data/views.
"""

from collections import Counter
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


def get_top_genres(favorite_artists):
    """
    Extracts genres from a list of favorite artists and returns the top 3 genres.

    Parameters:
        favorite_artists: List of favorite artists from Spotify API containing their genre info.

    Returns:
        List of the top 3 genres.
    """
    genres = []

    # Extract genres from each artist
    for artist in favorite_artists['items']:
        genres.extend(artist['genres'])

    # Count the occurrences of each genre
    genre_counts = Counter(genres)

    # Get the top 3 genres
    top_genres = genre_counts.most_common(3)

    # Return only the genre names (not the counts)
    return [genre for genre, count in top_genres]

def get_quirkiest_artists(favorite_artists):
    """
    Returns the 5 quirkiest artists based on their popularity scores.

    Parameters:
        - favorite_artists: a list of favorite artists
                (dictionaries with 'id', 'name', and 'popularity')

    Returns:
        A list of the 5 quirkiest artists based on popularity scores.
    """
    # Sort the artists by popularity (lower scores are quirkier)
    sorted_artists = sorted(favorite_artists['items'], key=lambda x: x['popularity'])

    # Return the top 5 quirkiest artists
    return sorted_artists[:5]
