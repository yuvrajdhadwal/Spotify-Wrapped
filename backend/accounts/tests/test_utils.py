import pytest
from django.utils import timezone
from unittest.mock import patch, MagicMock
from accounts.models import SpotifyToken
from accounts.utils import (
    get_user_tokens, 
    update_or_create_user_tokens, 
    is_spotify_authenticated, 
    refresh_spotify_token
)

@pytest.mark.django_db
def test_example_function():
    assert 1 + 1 == 2

@pytest.mark.django_db
def test_get_user_tokens(test_user):
    """
    Test the get_user_tokens function to ensure it correctly retrieves tokens.
    """
    # Create a SpotifyToken in the database
    token = SpotifyToken.objects.create(
        user=test_user,
        access_token='test_access_token',
        refresh_token='test_refresh_token',
        expires_in=timezone.now() + timezone.timedelta(seconds=3600),
        token_type='Bearer'
    )

    retrieved_token = get_user_tokens(test_user.username)
    assert retrieved_token.access_token == 'test_access_token'


@pytest.mark.django_db
def test_update_or_create_user_tokens(test_user):
    """
    Test the update_or_create_user_tokens function to create or update tokens.
    """
    session_id = test_user.username
    access_token = 'new_access_token'
    token_type = 'Bearer'
    expires_in = 3600
    refresh_token = 'new_refresh_token'

    # Initially, no tokens should exist
    assert get_user_tokens(session_id) is None

    # Call the update_or_create_user_tokens to create a new entry
    update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token)

    # Check that the token was created in the database
    token = get_user_tokens(session_id)
    assert token.access_token == 'new_access_token'

    # Update the token with new data
    update_or_create_user_tokens(session_id, 'updated_token', token_type, expires_in, refresh_token)

    # Verify that the token was updated
    token.refresh_from_db()
    assert token.access_token == 'updated_token'


@pytest.mark.django_db
@patch('accounts.utils.refresh_spotify_token')
def test_is_spotify_authenticated(mock_refresh_spotify_token, test_user):
    """
    Test the is_spotify_authenticated function to handle token expiry and refreshing.
    """
    # Create a SpotifyToken in the database with an expired token
    SpotifyToken.objects.create(
        user=test_user,
        access_token='test_access_token',
        refresh_token='test_refresh_token',
        expires_in=timezone.now() - timezone.timedelta(seconds=1),  # Expired
        token_type='Bearer'
    )

    # Call the is_spotify_authenticated, it should refresh the token
    assert is_spotify_authenticated(test_user.username) is True
    mock_refresh_spotify_token.assert_called_once_with(session_id=test_user.username)

@pytest.mark.django_db
@patch('accounts.utils.post')  # Patch 'post' in 'accounts.utils' module
def test_refresh_spotify_token(mock_post, test_user):
    """
    Test the refresh_spotify_token function to ensure it updates the user's tokens.
    """
    # Mock the response to return a valid JSON response and a 200 status code
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'access_token': 'new_access_token',
        'refresh_token': 'new_refresh_token',
        'token_type': 'Bearer',
        'expires_in': 3600
    }
    mock_response.status_code = 200  # Ensure status code is 200 (OK)
    mock_post.return_value = mock_response

    # Create an initial SpotifyToken
    SpotifyToken.objects.create(
        user=test_user,
        access_token='old_access_token',
        refresh_token='old_refresh_token',
        expires_in=timezone.now() - timezone.timedelta(seconds=1),  # Expired
        token_type='Bearer'
    )

    # Call the refresh_spotify_token function
    refresh_spotify_token(test_user.username)

    # Check that the token was updated correctly
    token = SpotifyToken.objects.get(user=test_user)
    assert token.access_token == 'new_access_token'
    assert token.refresh_token == 'new_refresh_token'