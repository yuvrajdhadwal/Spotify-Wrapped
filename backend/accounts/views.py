from django.shortcuts import render, redirect
import os
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from requests import Request, post
from .utils import update_or_create_user_tokens, is_spotify_authenticated

# Create your views here.

"""
Creates a class AuthURL which we use because we can have it take APIView as its parent
"""
class AuthURL(APIView):
    
    """
    Returns the url for the spotify api to get the user to give access to us because first 
    we need permission, then we can take data thus first this get method will ask for permission
    """
    def get(self, request, format=None):
        load_dotenv()

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': os.getenv('SCOPE'),
            'response_type': 'code',
            'redirect_url': os.getenv('REDIRECT_URI'),
            'client_id': os.getenv('CLIENT_ID')
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)

"""
Once the user has accepted the permissions and consent that spotify has given them based on the
scopes that we request, now we have to add them into our database. That is all this method does.
With the code given by permission, we use Spotify API to grab token details and then store them
in our model by creating/updating users based on session id
"""
def spotify_callback(request, format=None):
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

    update_or_create_user_tokens(request.session.session_key, access_token=access_token,
                                 token_type=token_type, refresh_token=refresh_token,
                                 expires_in=expires_in)
    
    # return redirect('frontend:') how to redirect to frontend webpage


"""
Again, utilizing the APIView from the rest api framework to check if a spotify user is authenticated
this will come in useful to call when we need to doublecheck that someone is logged in
"""
class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK )