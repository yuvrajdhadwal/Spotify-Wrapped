"""Tests methods from spotify_data/utils."""

from unittest.mock import patch
import unittest
import pytest
from ..utils import (get_spotify_user_data, get_user_favorite_artists, get_user_favorite_tracks,
                     get_top_genres, get_quirkiest_artists)


@pytest.mark.parametrize("status_code, expected_result", [
    (200, {'id': '123', 'display_name': 'Test User', 'email': 'test@example.com'}),
    (404, None),
    (401, None),
])
def test_get_spotify_user_data(status_code, expected_result):
    """Tests that a user's profile can be retrieved."""
    access_token = 'valid_token'
    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = status_code
        mock_response.json.return_value = {'id': '123',
            'display_name': 'Test User', 'email': 'test@example.com'} if status_code == 200 else {}

        result = get_spotify_user_data(access_token)
        assert result == expected_result


@pytest.mark.parametrize("status_code, expected_result", [
    (200, {'items': [{'name': 'Artist 1'}, {'name': 'Artist 2'}]}),
    (404, None),
])
def test_get_user_favorite_artists(status_code, expected_result):
    """Tests that a user's 20 favorites artists can be retrieved"""
    access_token = 'valid_token'
    timelimit = 'short_term'
    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = status_code
        mock_response.json.return_value = {
            'items': [{'name': 'Artist 1'}, {'name': 'Artist 2'}]} if status_code == 200 else {}

        result = get_user_favorite_artists(access_token, timelimit)
        assert result == expected_result

@pytest.mark.parametrize("status_code, expected_result", [
    (200, {'items': [{'name': 'Track 1'}, {'name': 'Track 2'}]}),
    (404, None),
])
def test_get_user_favorite_tracks(status_code, expected_result):
    """Tests that a user's 20 favorite tracks can be retrieved."""
    access_token = 'valid_token'
    timelimit = 'short_term'
    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = status_code
        mock_response.json.return_value = {
            'items': [{'name': 'Track 1'}, {'name': 'Track 2'}]} if status_code == 200 else {}

        result = get_user_favorite_tracks(access_token, timelimit)
        assert result == expected_result

class NonAPIFunctions(unittest.TestCase):
    """
    Functions that do not rely on a JSON response from the API.
    """
    def test_get_top_genres(self):
        """
        Tests that artists are properly filtered by top genre
        """
        # Mock data for favorite artists
        favorite_artists = {
            'items': [
                {'name': 'Artist A', 'genres': ['rock', 'pop']},
                {'name': 'Artist B', 'genres': ['pop', 'dance']},
                {'name': 'Artist C', 'genres': ['rock', 'indie']},
                {'name': 'Artist D', 'genres': ['jazz']},
                {'name': 'Artist E', 'genres': ['pop', 'jazz']},
            ]
        }

        # Expected output: top 3 genres
        expected_output = ['pop', 'rock', 'jazz']

        # Call the function
        result = get_top_genres(favorite_artists)

        # Assert that the result matches the expected output
        self.assertEqual(result, expected_output)

    def test_get_quirkiest_artists(self):
        """
        Tests that artists are properly filtered by lowest popularity
        """
        # Mock data for favorite artists with popularity scores
        favorite_artists = {
            'items': [
                {'id': '1', 'name': 'Artist A', 'popularity': 50},
                {'id': '2', 'name': 'Artist B', 'popularity': 20},
                {'id': '3', 'name': 'Artist C', 'popularity': 30},
                {'id': '4', 'name': 'Artist D', 'popularity': 10},
                {'id': '5', 'name': 'Artist E', 'popularity': 60},
                {'id': '6', 'name': 'Artist F', 'popularity': 5},
            ]
        }

        # Expected output: the 5 quirkiest artists (lowest popularity scores)
        expected_output = [
            {'id': '6', 'name': 'Artist F', 'popularity': 5},
            {'id': '4', 'name': 'Artist D', 'popularity': 10},
            {'id': '2', 'name': 'Artist B', 'popularity': 20},
            {'id': '3', 'name': 'Artist C', 'popularity': 30},
            {'id': '1', 'name': 'Artist A', 'popularity': 50},
        ]

        # Call the function
        result = get_quirkiest_artists(favorite_artists)

        # Assert that the result matches the expected output
        self.assertEqual(result, expected_output)
