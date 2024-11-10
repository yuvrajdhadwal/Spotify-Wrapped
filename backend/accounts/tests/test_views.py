'''Test for views'''
from unittest.mock import patch
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from accounts.views import (
    AuthURL,
    IsAuthenticated,
)

class AuthURLTest(TestCase):
    '''Testing setup'''
    def setUp(self):
        '''Setup'''
        self.client = Client()
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    @patch('os.getenv')
    def test_get_auth_url_success(self, mock_getenv):
        '''tests if we can get the proper auth_url'''
        mock_getenv.side_effect = lambda key: {
            'CLIENT_ID': 'test_client_id',
            'SCOPE': 'user-read-private',
            'REDIRECT_URI': 'http://localhost:8000/callback/'
        }.get(key, None)

        view = AuthURL.as_view()
        request = self.factory.get('/get-auth-url/')
        force_authenticate(request, user=self.user)

        response = view(request)
        self.assertEqual(response.status_code, 302)  # Redirect to Spotify auth URL
        self.assertIn('https://accounts.spotify.com/authorize', response.url)

    @patch('os.getenv')
    def test_get_auth_url_missing_env_vars(self, mock_getenv):
        '''Tests if code fails gracefully if env variables are missing'''
        mock_getenv.return_value = None  # Simulate missing environment variables

        view = AuthURL.as_view()
        request = self.factory.get('/get-auth-url/')
        force_authenticate(request, user=self.user)

        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertEqual(response.data['error'], 'Missing environment variables')

class SpotifyCallbackTest(TestCase):
    '''Testing callback function'''
    def setUp(self):
        '''Setup for callback issues'''
        self.client = Client()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    # @patch('os.getenv')
    # @patch('requests.post')
    # def test_spotify_callback_success(self, mock_post, mock_getenv):
    #     # Mock environment variables
    #     mock_getenv.side_effect = lambda key: {
    #         'CLIENT_ID': 'test_client_id',
    #         'CLIENT_SECRET': 'test_client_secret',
    #         'REDIRECT_URI': 'http://localhost:8000/callback/'
    #     }.get(key, None)

    #     # Mock Spotify token response
    #     mock_post.return_value.json.return_value = {
    #         'access_token': 'test_access_token',
    #         'token_type': 'Bearer',
    #         'expires_in': 3600,
    #         'refresh_token': 'test_refresh_token',
    #         'scope': 'user-read-private'
    #     }

    #     # Simulate user login
    #     self.client.login(username='testuser', password='testpass')

    #     # Simulate GET request with 'code' parameter
    #     response = self.client.get(
    #         reverse('spotify-callback'), {'code': 'test_code'}
    #     )

    #     # Verify redirect to frontend dashboard
    #     self.assertEqual(response.status_code, 200)

    #     # Verify that tokens are stored in the database
    #     tokens = SpotifyToken.objects.filter(username='testuser')
    #     self.assertTrue(tokens.exists())
    #     token = tokens.first()
    #     self.assertEqual(token.access_token, 'test_access_token')
    #     self.assertEqual(token.refresh_token, 'test_refresh_token')

    def test_spotify_callback_missing_code(self):
        '''Test to see if we gracefully handle missing code'''
        # Simulate user login
        self.client.login(username='testuser', password='testpass')

        # Simulate GET request without 'code' parameter
        response = self.client.get(reverse('spotify-callback'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Authentication Failed: Missing code parameter', response.content.decode())

    @patch('os.getenv')
    @patch('requests.post')
    def test_spotify_callback_error_response(self, mock_post, mock_getenv):
        '''Testing to see if proper error response'''
        # Mock environment variables
        mock_getenv.side_effect = lambda key: {
            'CLIENT_ID': 'test_client_id',
            'CLIENT_SECRET': 'test_client_secret',
            'REDIRECT_URI': 'http://localhost:8000/callback/'
        }.get(key, None)

        # Mock error response from Spotify
        mock_post.return_value.json.return_value = {
            'error': 'invalid_grant'
        }

        # Simulate user login
        self.client.login(username='testuser', password='testpass')

        # Simulate GET request with 'code' parameter
        response = self.client.get(reverse('spotify-callback'), {'code': 'test_code'})

        self.assertEqual(response.status_code, 200)
        self.assertIn('Authentication Failed: invalid_client', response.content.decode())

class IsAuthenticatedTest(TestCase):
    '''New test for the authenticated class'''
    def setUp(self):
        '''setup for the tests'''
        self.client = Client()
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    @patch('accounts.views.is_spotify_authenticated')
    def test_is_authenticated_true(self, mock_is_authenticated):
        '''tests to see if authentication works'''
        mock_is_authenticated.return_value = True

        view = IsAuthenticated.as_view()
        request = self.factory.get('/is-authenticated/')
        force_authenticate(request, user=self.user)

        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], True)

    @patch('accounts.views.is_spotify_authenticated')
    def test_is_authenticated_false(self, mock_is_authenticated):
        '''testing if authentication works'''
        mock_is_authenticated.return_value = False

        view = IsAuthenticated.as_view()
        request = self.factory.get('/is-authenticated/')
        force_authenticate(request, user=self.user)

        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], False)

class GetCSRFTokenTest(TestCase):
    '''testing the csrf token mehtod'''
    def setUp(self):
        '''setup'''
        self.client = Client()

    def test_get_csrf_token(self):
        '''simple test'''
        response = self.client.get(reverse('get_csrf_token'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'detail': 'CSRF cookie set'})

class SignInTest(TestCase):
    '''signin testing'''
    def setUp(self):
        '''setup'''
        self.client = Client()
        self.user_password = 'testpass'
        self.user = User.objects.create_user(username='testuser', password=self.user_password)

    def test_sign_in_success(self):
        '''testing if signin works'''
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': self.user_password
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Login successful'})

    def test_sign_in_invalid_credentials(self):
        '''testing if signin fails when invalid credentials'''
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'errors': {'login': 'Invalid username or password'}})

    def test_sign_in_invalid_method(self):
        '''testing when given completely wrong stuff'''
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {'error': 'Invalid request'})

class SignOutTest(TestCase):
    '''testing signout view'''
    def setUp(self):
        '''setting up the signout'''
        self.client = Client()
        self.user_password = 'testpass'
        self.user = User.objects.create_user(username='testuser', password=self.user_password)
        self.client.login(username='testuser', password=self.user_password)

    def test_sign_out(self):
        '''testing signout'''
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Logged Out'})

class SignUpTest(TestCase):
    '''testing for the signup function'''
    def setUp(self):
        '''setup'''
        self.client = Client()

    def test_sign_up_success(self):
        '''testing if it works'''
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'newuserpassword',
            'password2': 'newuserpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'sign-up sucessful'})
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_sign_up_password_mismatch(self):
        '''testing if it fails'''
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password1',
            'password2': 'password2'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('password2', response.json()['errors'])

    # def test_sign_up_short_username(self):
    #     response = self.client.post(reverse('register'), {
    #         'username': 'usr',
    #         'email': 'user@example.com',
    #         'password1': 'password123',
    #         'password2': 'password123'
    #     })
    #     self.assertEqual(response.status_code, 400)
    #     self.assertIn('username', response.json()['errors'])

    def test_sign_up_short_password(self):
        '''failing if short password'''
        response = self.client.post(reverse('register'), {
            'username': 'validusername',
            'email': 'user@example.com',
            'password1': '123',
            'password2': '123'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('password2', response.json()['errors'])

    # def test_sign_up_invalid_method(self):
    #     response = self.client.get(reverse('register'))
    #     self.assertEqual(response.status_code, 405)
    #     self.assertEqual(response.json(), {'error': 'Invalid request'})
