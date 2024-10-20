"""
Unit tests for views.py module.

This module contains extensive test cases for the views provided in views.py,
which handle Spotify authentication and authorization.

Tests cover various scenarios including successful retrieval of the authorization URL,
handling of the Spotify callback with valid and invalid data, and checking user
authentication status.

Dependencies are mocked to isolate tests and avoid external API calls or reliance
on environment variables.
"""
import unittest
import os
from unittest.mock import patch
from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.http import HttpResponse
from rest_framework import status
from rest_framework.test import APIClient
from accounts.views import spotify_callback
from requests import Request

class AuthURLTestCase(TestCase):
    """Test cases for the AuthURL view."""

    @patch('accounts.views.load_dotenv')
    @patch('accounts.views.os.getenv')
    def test_get_auth_url_success(self, mock_getenv, mock_load_dotenv):
        """
        Test that AuthURL GET request returns the correct Spotify authorization URL.
        """
        client_id = os.getenv('CLIENT_ID')
        scope = os.getenv('SCOPE')
        redirect_uri = os.getenv('REDIRECT_URI')

        # Mock environment variables
        mock_getenv.side_effect = lambda key: {'CLIENT_ID': client_id,
                                               'SCOPE': scope,
                                               'REDIRECT_URI': redirect_uri}.get(key)
        mock_load_dotenv.return_value = None

        # Make a GET request to the 'auth-url' endpoint
        client = APIClient()
        response = client.get(reverse('auth-url'))

        # Construct the expected URL
        expected_url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scope,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'client_id': client_id
        }).prepare().url

        # Check the response status and URL
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('url', response.data)
        self.assertEqual(response.data['url'], expected_url)

    @patch('accounts.views.os.getenv')
    def test_get_auth_url_missing_env_variables(self, mock_getenv):
        """
        Test that AuthURL handles missing environment variables gracefully.
        """
        mock_getenv.return_value = None  # Simulate missing env variables

        client = APIClient()
        response = client.get(reverse('auth-url'))

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Missing environment variables')

class SpotifyCallbackTestCase(TestCase):
    """Test cases for the spotify_callback view."""

    def setUp(self):
        self.factory = RequestFactory()
        self.session = self.client.session
        self.session.save()

    @patch('accounts.views.update_or_create_user_tokens')
    @patch('accounts.views.post')
    @patch('accounts.views.load_dotenv')
    @patch('accounts.views.os.getenv')
    def test_spotify_callback_success(self, mock_getenv, mock_load_dotenv, mock_post,
                                      mock_update_tokens):
        """
        Test that spotify_callback successfully processes the Spotify callback.
        """
        # Mock environment variables
        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        redirect_uri = os.getenv('REDIRECT_URI')
        mock_getenv.side_effect = lambda key: {'REDIRECT_URI': redirect_uri,
                                               'CLIENT_ID': client_id,
                                               'CLIENT_SECRET': client_secret}.get(key)
        mock_load_dotenv.return_value = None

        # Mock POST response from Spotify
        access_token = 'access_token'
        refresh_token = 'refresh_token'
        expires_in = 3600
        token_type = 'Bearer'

        mock_post.return_value.json.return_value = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': expires_in,
            'token_type': token_type
        }

        # Create a request with 'code' parameter
        request = self.factory.get('/spotify/redirect', {'code': 'auth_code'})
        request.session = self.session

        response = spotify_callback(request)

        # Assert that the response is an HttpResponse
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.content.decode(), "Authentication Successful")

        # Assert that tokens are updated
        mock_update_tokens.assert_called_once_with(
            request.session.session_key,
            access_token=access_token,
            token_type=token_type,
            refresh_token=refresh_token,
            expires_in=expires_in
        )

    @patch('accounts.views.post')
    @patch('accounts.views.load_dotenv')
    @patch('accounts.views.os.getenv')
    def test_spotify_callback_error(self, mock_getenv, mock_load_dotenv, mock_post):
        """
        Test that spotify_callback handles errors from Spotify.
        """
        # Mock environment variables
        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        redirect_uri = os.getenv('REDIRECT_URI')
        mock_getenv.side_effect = lambda key: {'REDIRECT_URI': redirect_uri,
                                               'CLIENT_ID': client_id,
                                               'CLIENT_SECRET': client_secret}.get(key)
        mock_load_dotenv.return_value = None

        # Mock POST response from Spotify with an error
        error_message = 'Invalid authorization code'
        mock_post.return_value.json.return_value = {'error': error_message}

        # Create a request with 'code' parameter
        request = self.factory.get('/spotify/redirect', {'code': 'invalid_code'})
        request.session = self.session

        response = spotify_callback(request)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.content.decode(), f"Authentication Failed: {error_message}")

    @patch('accounts.views.load_dotenv')
    @patch('accounts.views.os.getenv')
    def test_spotify_callback_missing_code(self, mock_getenv, mock_load_dotenv):
        """
        Test that spotify_callback handles missing 'code' parameter.
        """
        # Mock environment variables
        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        redirect_uri = os.getenv('REDIRECT_URI')
        mock_getenv.side_effect = lambda key: {'REDIRECT_URI': redirect_uri,
                                               'CLIENT_ID': client_id,
                                               'CLIENT_SECRET': client_secret}.get(key)
        mock_load_dotenv.return_value = None

        # Create a request without 'code' parameter
        request = self.factory.get('/spotify/redirect')
        request.session = self.session

        response = spotify_callback(request)

        # Since 'code' is missing, response should handle it gracefully
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.content.decode(), "Authentication Failed: Missing code parameter")

class IsAuthenticatedTestCase(TestCase):
    """Test cases for the IsAuthenticated view."""

    @patch('accounts.views.is_spotify_authenticated')
    def test_is_authenticated_true(self, mock_is_authenticated):
        """
        Test that IsAuthenticated returns True when user is authenticated.
        """
        mock_is_authenticated.return_value = True
        client = APIClient()
        response = client.get(reverse('is-authenticated'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': True})

    @patch('accounts.views.is_spotify_authenticated')
    def test_is_authenticated_false(self, mock_is_authenticated):
        """
        Test that IsAuthenticated returns False when user is not authenticated.
        """
        mock_is_authenticated.return_value = False
        client = APIClient()
        response = client.get(reverse('is-authenticated'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': False})

    @patch('accounts.views.is_spotify_authenticated')
    def test_is_authenticated_no_session(self, mock_is_authenticated):
        """
        Test that IsAuthenticated handles missing session key.
        """
        mock_is_authenticated.return_value = False
        client = APIClient()
        client.cookies.clear()  # Remove session cookies

        response = client.get(reverse('is-authenticated'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': False})

    @patch('accounts.views.is_spotify_authenticated')
    def test_is_authenticated_exception(self, mock_is_authenticated):
        """
        Test that IsAuthenticated handles exceptions gracefully.
        """
        mock_is_authenticated.side_effect = Exception("Unexpected error")
        client = APIClient()

        response = client.get(reverse('is-authenticated'))

        # Even if an exception occurs, we should handle it gracefully
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': False})

if __name__ == '__main__':
    unittest.main()
