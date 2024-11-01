"""
This module contains views for handling Spotify authentication and authorization.

It includes class-based views and function-based views to handle the Spotify OAuth flow, 
check user authentication status, and interact with the Spotify API.

Classes:
    - AuthURL: Returns the Spotify authorization URL to initiate OAuth.
    - IsAuthenticated: Checks if a user is authenticated with Spotify.
    
Functions:
    - spotify_callback: Handles the Spotify redirect after user authorization and stores tokens.
"""
import os
from django.shortcuts import HttpResponse
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from requests import Request, post
from spotify_data.views import update_or_add_spotify_user
from .utils import update_or_create_user_tokens, is_spotify_authenticated

# Create your views here.

class AuthURL(APIView):
    """
    Class-based view to handle Spotify authentication.

    This view returns a URL that directs the user to Spotify's authorization page.
    Once there, the user can grant permission to the app. This permission is required
    before we can interact with the user's Spotify data.

    Inherits from:
        APIView (rest_framework.views.APIView): Django Rest Framework class to handle API views.
    
    Methods:
        get(self, request): 
            Handles GET requests and constructs the Spotify authorization URL 
            with necessary parameters such as scope, response_type, and redirect URI.
    """

    def get(self, request):
        """
        Handles GET request to create the Spotify authorization URL.

        Loads environment variables to fetch Spotify client credentials and scopes.
        Constructs a URL using the Spotify authorization endpoint and returns it
        in the response.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response (rest_framework.response.Response): 
                A JSON response containing the Spotify authorization URL.
        """
        load_dotenv()

        client_id = os.getenv('CLIENT_ID')
        scope = os.getenv('SCOPE')
        redirect_uri = os.getenv('REDIRECT_URI')

        if not client_id or not scope or not redirect_uri:
            return Response({'error': 'Missing environment variables'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scope,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'client_id': client_id
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)

def spotify_callback(request, format=None):
    """
    View to handle the callback from Spotify after user authorization.

    This view processes the authorization code received from Spotify and exchanges
    it for access and refresh tokens, which are stored in the database. This allows 
    future interactions with Spotify on behalf of the user.

    Parameters:
        request (HttpRequest): The HTTP request object containing the Spotify callback data.
    
    Returns:
        HttpResponse: Redirects the user to a frontend webpage or handles any errors.

    Notes:
        - The authorization code is extracted from the request URL.
        - Access and refresh tokens are obtained by making a POST request to Spotify's token
            endpoint.
        - Tokens are stored using the `update_or_create_user_tokens` utility.
    """
    load_dotenv()
    code = request.GET.get('code')

    if not code:
        return HttpResponse("Authentication Failed: Missing code parameter")

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.getenv('REDIRECT_URI'),
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET')
    }, timeout=10).json()

    if 'error' in response:
        return HttpResponse(f"Authentication Failed: {response['error']}")

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')

    if not request.session.exists(request.session.session_key):
        request.session.create()
    session_id = request.session.session_key

    # resolved: continue using session key
    update_or_create_user_tokens(session_id, access_token=access_token,
                                 token_type=token_type, refresh_token=refresh_token,
                                 expires_in=expires_in)

    # Add the user to database, or update user info
    # update_or_add_spotify_user(request, session_id)

    # TODO: Redirect to a frontend page after successful token storage
    # return redirect('frontend:') how to redirect to frontend webpage
    return HttpResponse("Authentication Successful")


class IsAuthenticated(APIView):
    """
    Class-based view to check if the current user is authenticated with Spotify.

    This view verifies whether the user has valid Spotify tokens and is currently
    authenticated. It can be used to check if API calls to Spotify should be allowed
    for a user.

    Methods:
        get(self, request, format=None): 
            Handles GET requests and returns the authentication status of the user.
    """

    def get(self, request):
        """
        Handles GET request to check if the user is authenticated with Spotify.

        Uses the session key to check if the user has valid tokens stored in the database.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response (rest_framework.response.Response): 
                A JSON response indicating the authentication status (True/False).
        """
        # resolved: continue using session key
        try:
            is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        except Exception:
            is_authenticated = False
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)
