import pytest
import json

from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from unittest.mock import patch
from spotify_data.views import update_or_add_spotify_user
from accounts.models import SpotifyToken
from django.core.exceptions import ObjectDoesNotExist


@pytest.fixture
def user():
    """Fixture to create a user instance."""
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def mock_request(mocker):
    """Fixture to mock the request object."""
    mock = mocker.Mock()
    mock.user = mocker.Mock()  # Mock user object
    return mock


@pytest.fixture
def session_id():
    return "test_session_id"


@pytest.fixture
def mock_token():
    return {
        'access_token': 'test_access_token',
        'expires_in': timezone.now() + timezone.timedelta(seconds=3600),  # 1 hour
        'refresh_token': 'test_refresh_token',
        'token_type': 'Bearer'
    }


@pytest.fixture
def mock_user_data():
    return {
        'id': 'spotify_user_id',
        'display_name': 'Test User',
        'email': 'testuser@example.com',
        'images': [{'url': 'http://example.com/image.jpg'}]
    }

@pytest.mark.django_db
def test_user_not_authenticated(mock_request, session_id):
    """Test when user is not authenticated."""
    with patch('accounts.views.is_spotify_authenticated', return_value=False):
        response = update_or_add_spotify_user(mock_request, session_id)
        assert response.status_code == 403
        assert json.loads(response.content) == {'error': 'User not authenticated'}

@pytest.mark.django_db
def test_missing_access_token(mock_request, session_id, user):
    """Test when access token does not exist."""

    # Set the mock request user to the actual user instance
    mock_request.user = user

    with patch('accounts.utils.is_spotify_authenticated', return_value=True), \
            patch('accounts.models.SpotifyToken.objects.get', side_effect=ObjectDoesNotExist):
        response = update_or_add_spotify_user(mock_request, session_id)
        assert response.status_code == 500
        assert response.content == b"User add/update failed: missing access token"

@pytest.mark.django_db
def test_token_expired_and_refreshed(mock_request, session_id, mock_token, mock_user_data):
    """Test when the token is expired and needs to be refreshed."""
    token_entry = SpotifyToken(user=session_id, access_token='old_access_token',
                               expires_in=timezone.now() - timezone.timedelta(seconds=1))

    with patch('accounts.views.is_spotify_authenticated', return_value=True), \
            patch('accounts.models.SpotifyToken.objects.get', return_value=token_entry), \
            patch('accounts.utils.refresh_spotify_token', return_value=None), \
            patch('spotify_data.views.get_spotify_user_data', return_value=mock_user_data):
        response = update_or_add_spotify_user(mock_request, session_id)
        assert response.status_code == 200
        assert 'spotify_user' in response.json()

@pytest.mark.django_db
def test_successful_user_update(mock_request, session_id, mock_token, mock_user_data, user):
    """Test successful user update when the user already exists."""
    mock_request.user = user

    # Create the token with a valid datetime for expires_in
    token_entry = SpotifyToken.objects.create(
        user=session_id,
        access_token=mock_token['access_token'],
        expires_in=timezone.now() + timezone.timedelta(seconds=3600)  # 1 hour from now
    )

    with patch('accounts.views.is_spotify_authenticated', return_value=True), \
            patch('accounts.models.SpotifyToken.objects.get', return_value=token_entry), \
            patch('spotify_data.views.get_spotify_user_data', return_value=mock_user_data):
        response = update_or_add_spotify_user(mock_request, session_id)
        assert response.status_code == 200
        assert 'spotify_user' in json.loads(response.content)

@pytest.mark.django_db
def test_failed_user_data_fetch(mock_request, session_id, mock_token):
    """Test when fetching user data from Spotify fails."""
    token_entry = SpotifyToken(user=session_id, access_token=mock_token['access_token'],
                               expires_in=timezone.now() + timezone.timedelta(seconds=3600))
    SpotifyToken.objects.create(user=session_id, **mock_token)

    with patch('accounts.views.is_spotify_authenticated', return_value=True), \
            patch('accounts.models.SpotifyToken.objects.get', return_value=token_entry), \
            patch('spotify_data.views.get_spotify_user_data', return_value=None):
        response = update_or_add_spotify_user(mock_request, session_id)
        assert response.status_code == 500
        assert json.loads(response.content) == {'error': 'Could not fetch user data from Spotify'}

