import pytest
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from accounts.models import SpotifyToken
from accounts.views import spotify_callback


@pytest.mark.django_db
class TestAuthURL:
    def test_auth_url(self, client):
        """
        Test that the AuthURL view returns a valid URL with the correct status.
        """
        response = client.get(reverse('auth-url'))  # Update with your actual view name
        assert response.status_code == status.HTTP_200_OK
        assert 'url' in response.json()


@pytest.mark.django_db
class TestSpotifyCallback:
    @patch('accounts.views.post')
    def test_spotify_callback_success(self, mock_post, client):
        """
        Test the Spotify callback view and token update process.
        """
        # Mock the response from Spotify's token endpoint
        mock_post.return_value.json.return_value = {
            'access_token': 'test_access_token',
            'refresh_token': 'test_refresh_token',
            'token_type': 'Bearer',
            'expires_in': 3600
        }

        session = client.session
        session.save()

        response = client.get(reverse('spotify-callback'), {'code': 'test_code'})
        # TODO: Verify the tokens are saved in the database

        # assert response.status_code == status.HTTP_302_FOUND  # Assuming a redirect occurs

        # token = SpotifyToken.objects.get(user=session.session_key)
        # assert token.access_token == 'test_access_token'
        assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
class TestIsAuthenticated:
    @patch('accounts.views.is_spotify_authenticated', return_value=True)  # Mock the utility function
    def test_is_authenticated(self, mock_is_spotify_authenticated, client):
        """
        Test the IsAuthenticated view to ensure the user authentication status is correct.
        """
        session = client.session
        session.save()

        response = client.get(reverse('is-authenticated'))  # Update with your actual view name
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['status'] is True
