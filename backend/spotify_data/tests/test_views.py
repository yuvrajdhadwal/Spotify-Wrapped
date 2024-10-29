from unittest.mock import patch, MagicMock
import json
import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from spotify_data.views import update_or_add_spotify_user
from accounts.models import SpotifyToken


@pytest.fixture
def create_user():
    """Fixture to create a user instance."""
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def mock_request_obj(mocker):
    """Fixture to mock the request object."""
    mock = mocker.Mock()
    mock.user = mocker.Mock()  # Mock user object
    return mock


@pytest.fixture
def create_session_id():
    """Instantiates test session id."""
    return "test_session_id"


@pytest.fixture
def create_mock_token():
    """Instantiates test access token."""
    return {
        'access_token': 'test_access_token',
        'expires_in': timezone.now() + timezone.timedelta(seconds=3600),  # 1 hour
        'refresh_token': 'test_refresh_token',
        'token_type': 'Bearer'
    }


@pytest.fixture
def create_mock_user_data():
    """Instantiates test user data."""
    return {
        'id': 'spotify_user_id',
        'display_name': 'Test User',
        'email': 'testuser@example.com',
        'images': [{'url': 'http://example.com/image.jpg'}]
    }

@pytest.mark.django_db
def test_user_not_authenticated(mock_request_obj, create_session_id):
    """Test when user is not authenticated."""
    with patch('accounts.views.is_spotify_authenticated', return_value=False):
        response = update_or_add_spotify_user(mock_request_obj, create_session_id)
        assert response.status_code == 403
        assert json.loads(response.content) == {'error': 'User not authenticated'}


@pytest.mark.django_db
def test_missing_access_token(mock_request_obj, create_session_id, create_user):
    """Test when access token does not exist."""

    mock_request_obj.user = create_user

    # Patch the is_spotify_authenticated function
    with patch('accounts.views.is_spotify_authenticated', return_value=True), \
            patch('accounts.models.SpotifyToken.objects.get', side_effect=ObjectDoesNotExist):
        response = update_or_add_spotify_user(mock_request_obj, create_session_id)

        assert response.status_code == 403  # Adjusted to match the expected behavior
        assert json.loads(response.content) == {'error': 'User not authenticated'}


@pytest.mark.django_db
def test_successful_user_update(mock_request_obj, create_session_id, create_mock_token,
                                create_mock_user_data, create_user):
    """Test successful user update when the user already exists."""
    mock_request_obj.user = create_user

    # Create the token with a valid datetime for expires_in
    token_entry = SpotifyToken.objects.create(
        user=create_session_id,
        access_token=create_mock_token['access_token'],
        expires_in=timezone.now() + timezone.timedelta(seconds=3600)  # 1 hour from now
    )

    with patch('accounts.views.is_spotify_authenticated', return_value=True), \
            patch('accounts.models.SpotifyToken.objects.get', return_value=token_entry), \
            patch('spotify_data.views.get_spotify_user_data', return_value=create_mock_user_data):
        response = update_or_add_spotify_user(mock_request_obj, create_session_id)
        assert response.status_code == 200
        assert 'spotify_user' in json.loads(response.content)


@pytest.mark.django_db
def test_failed_user_data_fetch(mock_request_obj, create_session_id, create_mock_token):
    """Test when fetching user data from Spotify fails."""
    token_entry = SpotifyToken(user=create_session_id, access_token=create_mock_token['access_token'],
                               expires_in=timezone.now() + timezone.timedelta(seconds=3600))
    SpotifyToken.objects.create(user=create_session_id, **create_mock_token)

    with patch('accounts.views.is_spotify_authenticated', return_value=True), \
            patch('accounts.models.SpotifyToken.objects.get', return_value=token_entry), \
            patch('spotify_data.views.get_spotify_user_data', return_value=None):
        response = update_or_add_spotify_user(mock_request_obj, create_session_id)
        assert response.status_code == 500
        assert json.loads(response.content) == {'error': 'Could not fetch user data from Spotify'}


@pytest.mark.django_db
def test_llm_api_call(mock_request_obj, create_session_id, create_mock_token,
                      create_mock_user_data, create_user):
    """Test successful LLM API call and description generation."""
    mock_request_obj.user = create_user

    # Create the token with a valid datetime for expires_in
    token_entry = SpotifyToken.objects.create(
        user=create_session_id,
        access_token=create_mock_token['access_token'],
        expires_in=timezone.now() + timezone.timedelta(seconds=3600)  # 1 hour from now
    )

    with patch('accounts.views.is_spotify_authenticated', return_value=True), \
            patch('accounts.models.SpotifyToken.objects.get', return_value=token_entry), \
            patch('spotify_data.views.get_spotify_user_data', return_value=create_mock_user_data), \
            patch('spotify_data.views.get_user_favorite_tracks', return_value=['track1', 'track2']), \
            patch('spotify_data.views.get_user_favorite_artists', return_value=['artist1', 'artist2']), \
            patch('groq.Groq.chat.completions.create') as mock_llm_api:
        # Simulate LLM response
        mock_llm_api.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Test dynamic description"))])

        response = update_or_add_spotify_user(mock_request_obj, create_session_id)

        # Check response status
        assert response.status_code == 200

        # Check if LLM API was called with expected prompt
        mock_llm_api.assert_called_once()
        call_args = mock_llm_api.call_args[1]  # Get the second argument (kwargs)
        assert "Describe how someone who listens to artists like artist1, artist2 tends to act" in \
               call_args['messages'][1]['content']

        # Check if description is present in the response
        response_data = json.loads(response.content)
        assert response_data['spotify_user']['description'] == "Test dynamic description"
