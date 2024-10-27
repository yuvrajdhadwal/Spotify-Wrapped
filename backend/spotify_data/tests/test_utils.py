import pytest
from unittest.mock import patch
from ..utils import get_spotify_user_data, get_user_favorite_artists, get_user_favorite_tracks


@pytest.mark.parametrize("status_code, expected_result", [
    (200, {'id': '123', 'display_name': 'Test User', 'email': 'test@example.com'}),
    (404, None),
    (401, None),
])
def test_get_spotify_user_data(status_code, expected_result):
    access_token = 'valid_token'
    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = status_code
        mock_response.json.return_value = {'id': '123', 'display_name': 'Test User',
                                           'email': 'test@example.com'} if status_code == 200 else {}

        result = get_spotify_user_data(access_token)
        assert result == expected_result


@pytest.mark.parametrize("status_code, expected_result", [
    (200, {'items': [{'name': 'Artist 1'}, {'name': 'Artist 2'}]}),
    (404, None),
])
def test_get_user_favorite_artists(status_code, expected_result):
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
    access_token = 'valid_token'
    timelimit = 'short_term'
    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = status_code
        mock_response.json.return_value = {
            'items': [{'name': 'Track 1'}, {'name': 'Track 2'}]} if status_code == 200 else {}

        result = get_user_favorite_tracks(access_token, timelimit)
        assert result == expected_result