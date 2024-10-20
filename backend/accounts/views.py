from django.shortcuts import render, redirect
import os
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from requests import Request, post
from .utils import update_or_create_user_tokens, is_spotify_authenticated
from django.shortcuts import HttpResponse

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
        get(self, request, format=None): 
            Handles GET requests and constructs the Spotify authorization URL 
            with necessary parameters such as scope, response_type, and redirect URI.
    """
    
    def get(self, request, format=None):
        """
        Handles GET request to create the Spotify authorization URL.

        Loads environment variables to fetch Spotify client credentials and scopes.
        Constructs a URL using the Spotify authorization endpoint and returns it
        in the response.

        Parameters:
            request (HttpRequest): The HTTP request object.
            format (str, optional): Response format (defaults to None).

        Returns:
            Response (rest_framework.response.Response): 
                A JSON response containing the Spotify authorization URL.
        """
        load_dotenv()

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': os.getenv('SCOPE'),
            'response_type': 'code',
            'redirect_url': os.getenv('REDIRECT_URI'),
            'client_id': os.getenv('CLIENT_ID')
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
        format (str, optional): Response format (defaults to None).
    
    Returns:
        HttpResponse: Redirects the user to a frontend webpage or handles any errors.

    Notes:
        - The authorization code is extracted from the request URL.
        - Access and refresh tokens are obtained by making a POST request to Spotify's token endpoint.
        - Tokens are stored using the `update_or_create_user_tokens` utility.
    """
    load_dotenv()
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.getenv('REDIRECT_URI'),
        'client_id': os.getenv('CLIENT_ID'),
        'client_secret': os.getenv('CLIENT_SECRET')
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    # TODO: Might switch session key with user_id, unsure for now
    update_or_create_user_tokens(request.session.session_key, access_token=access_token,
                                 token_type=token_type, refresh_token=refresh_token,
                                 expires_in=expires_in)
    
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

    def get(self, request, format=None):
        """
        Handles GET request to check if the user is authenticated with Spotify.

        Uses the session key to check if the user has valid tokens stored in the database.

        Parameters:
            request (HttpRequest): The HTTP request object.
            format (str, optional): Response format (defaults to None).

        Returns:
            Response (rest_framework.response.Response): 
                A JSON response indicating the authentication status (True/False).
        """
        # TODO: Are we still using session key? or user data unsure
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK )