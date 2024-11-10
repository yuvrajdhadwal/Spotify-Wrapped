# """
# Unit tests for spotify_tokens.py module.

# This module contains extensive test cases for the utility functions provided in spotify_tokens.py,
# which manage Spotify authentication tokens for users.

# Tests cover various scenarios including successful retrieval, creation, updating, and refreshing
# of Spotify tokens, as well as handling of edge cases and errors.

# Dependencies are mocked to isolate tests and avoid external API calls or database interactions.
# """

# import unittest
# from unittest.mock import patch, MagicMock
# from datetime import timedelta
# from django.utils import timezone
# from django.test import TestCase
# from requests.exceptions import RequestException
# from accounts.utils import (
#     get_user_tokens,
#     update_or_create_user_tokens,
#     is_spotify_authenticated,
#     refresh_spotify_token
# )

# class SpotifyTokensTestCase(TestCase):
#     """Test cases for Spotify token management functions."""

#     @patch('accounts.models.SpotifyToken.objects')
#     def test_get_user_tokens_exists(self, mock_objects):
#         """
#         Test that get_user_tokens returns the token when it exists in the database.
#         """
#         session_id = 'test_session'
#         token = MagicMock()

#         # Create a mock queryset
#         mock_queryset = MagicMock()
#         mock_queryset.exists.return_value = True
#         mock_queryset.__getitem__.return_value = token  # So user_tokens[0] returns token

#         # Set the return value of filter to be the mock queryset
#         mock_objects.filter.return_value = mock_queryset

#         result = get_user_tokens(session_id)

#         mock_objects.filter.assert_called_with(user=session_id)
#         self.assertEqual(result, token)

#     @patch('accounts.models.SpotifyToken.objects')
#     def test_get_user_tokens_not_exists(self, mock_objects):
#         """
#         Test that get_user_tokens returns None when the token does not exist.
#         """
#         session_id = 'test_session'
#         mock_objects.filter.return_value.exists.return_value = False

#         result = get_user_tokens(session_id)

#         mock_objects.filter.assert_called_with(user=session_id)
#         self.assertIsNone(result)

#     @patch('accounts.utils.get_user_tokens')
#     def test_update_or_create_user_tokens_update(self, mock_get_user_tokens):
#         """
#         Test that update_or_create_user_tokens updates existing tokens.
#         """
#         session_id = 'test_session'
#         access_token = 'new_access_token'
#         token_type = 'Bearer'
#         expires_in = 3600
#         refresh_token = 'new_refresh_token'

#         existing_token = MagicMock()
#         mock_get_user_tokens.return_value = existing_token

#         update_or_create_user_tokens(session_id, access_token, token_type, expires_in,
#                                      refresh_token)

#         self.assertEqual(existing_token.access_token, access_token)
#         self.assertEqual(existing_token.token_type, token_type)
#         self.assertEqual(existing_token.refresh_token, refresh_token)
#         self.assertTrue(existing_token.expires_in > timezone.now())
#         existing_token.save.assert_called_once()

#     @patch('accounts.utils.get_user_tokens')
#     @patch('accounts.utils.SpotifyToken')
#     def test_update_or_create_user_tokens_create(self, mock_spotifytoken, mock_get_user_tokens):
#         """
#         Test that update_or_create_user_tokens creates new tokens when none exist.
#         """
#         session_id = 'test_session'
#         access_token = 'new_access_token'
#         token_type = 'Bearer'
#         expires_in = 3600
#         refresh_token = 'new_refresh_token'

#         mock_get_user_tokens.return_value = None

#         update_or_create_user_tokens(session_id, access_token, token_type, expires_in,
#                                      refresh_token)
#         expected_expires_in =(timezone.now()
#                               + timedelta(seconds=expires_in)).replace(microsecond=0)
#         actual_expires_in = mock_spotifytoken.call_args[1]['expires_in'].replace(microsecond=0)
#         assert actual_expires_in == expected_expires_in

#         mock_spotifytoken.assert_called_once_with(
#             user=session_id,
#             access_token=access_token,
#             token_type=token_type,
#             expires_in=mock_spotifytoken.call_args[1]['expires_in'],
#             refresh_token=refresh_token
#         )
#         mock_spotifytoken.return_value.save.assert_called_once()

#     @patch('accounts.utils.refresh_spotify_token')
#     @patch('accounts.utils.get_user_tokens')
#     def test_is_spotify_authenticated_valid_token(self, mock_get_user_tokens, mock_refresh_token):
#         """
#         Test that is_spotify_authenticated returns True when token is valid.
#         """
#         session_id = 'test_session'
#         token = MagicMock()
#         token.expires_in = timezone.now() + timedelta(seconds=3600)
#         mock_get_user_tokens.return_value = token

#         result = is_spotify_authenticated(session_id)

#         self.assertTrue(result)
#         mock_refresh_token.assert_not_called()

#     @patch('accounts.utils.refresh_spotify_token')
#     @patch('accounts.utils.get_user_tokens')
#     def test_is_spotify_authenticated_expired_token(self, mock_get_user_tokens, mock_refresh_token):
#         """
#         Test that is_spotify_authenticated refreshes token when expired.
#         """
#         session_id = 'test_session'
#         token = MagicMock()
#         token.expires_in = timezone.now() - timedelta(seconds=3600)
#         mock_get_user_tokens.return_value = token

#         result = is_spotify_authenticated(session_id)

#         self.assertTrue(result)
#         mock_refresh_token.assert_called_once_with(session_id=session_id)

#     @patch('accounts.utils.get_user_tokens')
#     def test_is_spotify_authenticated_no_token(self, mock_get_user_tokens):
#         """
#         Test that is_spotify_authenticated returns False when no token exists.
#         """
#         session_id = 'test_session'
#         mock_get_user_tokens.return_value = None

#         result = is_spotify_authenticated(session_id)

#         self.assertFalse(result)

#     @patch('accounts.utils.update_or_create_user_tokens')
#     @patch('accounts.utils.post')
#     @patch('accounts.utils.get_user_tokens')
#     @patch('accounts.utils.os.getenv')
#     @patch('accounts.utils.load_dotenv')
#     def test_refresh_spotify_token_success(self, mock_load_dotenv, mock_getenv,
#                                            mock_get_user_tokens, mock_post, mock_update_tokens):
#         """
#         Test that refresh_spotify_token successfully refreshes the token.
#         """
#         session_id = 'test_session'
#         refresh_token = 'refresh_token'
#         access_token = 'new_access_token'
#         token_type = 'Bearer'
#         expires_in = 3600

#         mock_get_user_tokens.return_value = MagicMock(refresh_token=refresh_token)
#         mock_getenv.side_effect = lambda key: {'CLIENT_ID': 'client_id',
#                                                'CLIENT_SECRET': 'client_secret'}.get(key)
#         mock_post.return_value.json.return_value = {
#             'access_token': access_token,
#             'token_type': token_type,
#             'expires_in': expires_in,
#             'refresh_token': refresh_token
#         }

#         refresh_spotify_token(session_id)

#         mock_load_dotenv.assert_called_once()
#         mock_post.assert_called_once_with(
#             'https://accounts.spotify.com/api/tokens',
#             data={
#                 'grant_type': 'refresh_token',
#                 'refresh_token': refresh_token,
#                 'client_id': 'client_id',
#                 'client_secret': 'client_secret'
#             },
#             timeout=10
#         )
#         mock_update_tokens.assert_called_once_with(
#             session_id=session_id,
#             access_token=access_token,
#             token_type=token_type,
#             expires_in=expires_in,
#             refresh_token=refresh_token
#         )

#     @patch('accounts.utils.update_or_create_user_tokens')
#     @patch('accounts.utils.post')
#     @patch('accounts.utils.get_user_tokens')
#     @patch('accounts.utils.os.getenv')
#     @patch('accounts.utils.load_dotenv')
#     def test_refresh_spotify_token_failure(self, mock_load_dotenv, mock_getenv,
#                                            mock_get_user_tokens, mock_post, mock_update_tokens):
#         """
#         Test that refresh_spotify_token handles failure to refresh token.
#         """
#         session_id = 'test_session'
#         refresh_token = 'invalid_refresh_token'

#         mock_get_user_tokens.return_value = MagicMock(refresh_token=refresh_token)
#         mock_getenv.side_effect = lambda key: {'CLIENT_ID': 'client_id',
#                                                'CLIENT_SECRET': 'client_secret'}.get(key)
#         mock_post.return_value.json.return_value = {}  # Simulate failure

#         refresh_spotify_token(session_id)

#         mock_load_dotenv.assert_called_once()
#         mock_post.assert_called_once()
#         mock_update_tokens.assert_called_once_with(
#             session_id=session_id,
#             access_token=None,
#             token_type=None,
#             expires_in=None,
#             refresh_token=None
#         )

#     @patch('accounts.utils.post')
#     @patch('accounts.utils.get_user_tokens')
#     @patch('accounts.utils.os.getenv')
#     @patch('accounts.utils.load_dotenv')
#     def test_refresh_spotify_token_network_error(self, mock_load_dotenv, mock_getenv,
#                                                  mock_get_user_tokens, mock_post):
#         """
#         Test that refresh_spotify_token handles network errors gracefully.
#         """
#         session_id = 'test_session'
#         refresh_token = 'refresh_token'

#         mock_get_user_tokens.return_value = MagicMock(refresh_token=refresh_token)
#         mock_getenv.side_effect = lambda key: {'CLIENT_ID': 'client_id',
#                                                'CLIENT_SECRET': 'client_secret'}.get(key)
#         mock_post.side_effect = RequestException("Network error")

#         with self.assertRaises(RequestException):
#             refresh_spotify_token(session_id)

#         mock_load_dotenv.assert_called_once()
#         mock_post.assert_called_once()

#     @patch('accounts.models.SpotifyToken.objects')
#     def test_get_user_tokens_invalid_session_id(self, mock_objects):
#         """
#         Test get_user_tokens with an invalid session_id.
#         """
#         session_id = None
#         mock_objects.filter.return_value.exists.return_value = False

#         result = get_user_tokens(session_id)

#         mock_objects.filter.assert_called_with(user=session_id)
#         self.assertIsNone(result)

#     @patch('accounts.utils.get_user_tokens')
#     @patch('accounts.utils.load_dotenv')
#     def test_refresh_spotify_token_missing_env_variables(self, mock_load_dotenv,
#                                                          mock_get_user_tokens):
#         """
#         Test that refresh_spotify_token handles missing environment variables.
#         """
#         session_id = 'test_session'
#         refresh_token = 'refresh_token'

#         # Mock the return value of get_user_tokens
#         mock_get_user_tokens.return_value = MagicMock(refresh_token=refresh_token)
#         # Mock load_dotenv to prevent loading actual environment variables
#         mock_load_dotenv.return_value = None

#         # Clear environment variables
#         with patch.dict('os.environ', {}, clear=True):
#             with self.assertRaises(TypeError):
#                 refresh_spotify_token(session_id)

#     # Add more test cases here when frontend is made

# if __name__ == '__main__':
#     unittest.main()
