"""
Utils used in spotify_data/views.
"""

from collections import Counter
import requests
from groq import Groq,  GroqError


SPOTIFY_RECOMMENDATIONS_URL = "https://api.spotify.com/v1/recommendations"

def get_spotify_user_data(access_token):
    """
    Retrieves current user data including Spotify ID, email, profile image, and username.

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
    for artist in favorite_artists['items']:
        genres.extend(artist['genres'])

    genre_counts = Counter(genres)
    top_genres = genre_counts.most_common(3)
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
    sorted_artists = sorted(favorite_artists['items'], key=lambda x: x['popularity'])
    return sorted_artists[:5]

def create_groq_description(groq_api_key, favorite_artists):
    """
    Create a description of user tastes/ lifestyle based on favorite artists

    Args:
        - groq_api_key: the groq api key
        - favorite_artists: List of favorite artists
        (dictionaries with 'id', 'name', and 'popularity')

    Returns:
        - llama_description: the description construced by the LLM

    """
    if not groq_api_key:
        raise GroqError("GROQ_API_KEY environment variable is not set.")

    client = Groq(api_key=groq_api_key)
    description_prompt = (
        f"Describe how someone who listens to artists like {', '.join(favorite_artists)} "
        "tends to act, think, and dress."
    )

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": ("You are a music analyst who "
                                "describes user behavior based on their music tastes.",
                                )
                },
                {
                    "role": "user",
                    "content": description_prompt
                }
            ],
            model="llama3-8b-8192",
        )

        llama_description = response.choices[0].message.content
    except KeyError as e:
        llama_description = f"Key error: {str(e)}"
    except Exception as e:
        llama_description = f"Description unavailable due to API error: {str(e)}"  # pylint: disable=broad-exception-caught
    return llama_description

def get_spotify_recommendations(user_token, seed_artists=None,
                                seed_tracks=None, seed_genres=None, target_attributes=None):
    """
    Fetches a list of recommended songs from Spotify based on provided seeds and target attributes.

    Args:
        user_token (str): The Spotify access token for the user.
        seed_artists (list of str): List of Spotify artist IDs to base recommendations on.
        seed_tracks (list of str): List of Spotify track IDs to base recommendations on.
        seed_genres (list of str): List of genres to base recommendations on.
        target_attributes (dict): Dictionary of target musical attributes
        (e.g., `target_energy`, `target_valence`).

    Returns:
        list: A list of recommended songs, where each song
        is represented as a dictionary with details.
    """
    headers = {
        "Authorization": f"Bearer {user_token}"
    }

    params = {
        "limit": 20,
    }
    if seed_artists:
        params["seed_artists"] = ",".join(seed_artists)
    if seed_tracks:
        params["seed_tracks"] = ",".join(seed_tracks)
    if seed_genres:
        params["seed_genres"] = ",".join(seed_genres)
    if target_attributes:
        params.update(target_attributes)

    try:
        response = requests.get(SPOTIFY_RECOMMENDATIONS_URL,
                                headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        recommended_songs = [
            {
                "id": track["id"],
                "name": track["name"],
                "artist": ", ".join([artist["name"] for artist in track["artists"]]),
                "album": track["album"]["name"],
                "preview_url": track["preview_url"],
                "external_url": track["external_urls"]["spotify"]
            }
            for track in data["tracks"]
        ]
        return recommended_songs

    except requests.exceptions.RequestException as e:
        print(f"Error fetching recommendations: {e}")
        return []
