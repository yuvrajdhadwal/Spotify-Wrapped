"""
This module defines the model for storing Spotify tokens in the database.

The `SpotifyToken` model is used to store access tokens for Spotify users, 
including the necessary information to refresh tokens when they expire.

Classes:
    - SpotifyToken: A Django model that stores information about a user's 
      Spotify access token, refresh token, and expiration time.

Attributes:
    - user (CharField): A unique identifier for the user associated with the token.
    - created_at (DateTimeField): The timestamp when the token was created.
    - refresh_token (CharField): The token used to refresh the user's access when it expires.
    - access_token (CharField): The current access token for the user.
    - expires_in (DateTimeField): The timestamp when the access token will expire.
    - token_type (CharField): The type of token issued (e.g., Bearer).
"""

from django.db import models

class SpotifyToken(models.Model):
    """
    A model to represent the Spotify access and refresh tokens for a user.

    This model stores the necessary details for each user's Spotify authentication,
    such as the access token, refresh token, expiration time, and token type.
    
    Attributes:
        user (CharField): The unique identifier for the user (session ID).
        created_at (DateTimeField): The time when the token entry was created in the database.
        refresh_token (CharField): The refresh token that allows generating new access tokens.
        access_token (CharField): The current access token for interacting with Spotify's API.
        expires_in (DateTimeField): The timestamp when the access token expires.
        token_type (CharField): The type of token provided by Spotify (e.g., Bearer).
    """
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

    class Meta:
        """
        Metadata options for the SpotifyToken model.

        Attributes:
            app_label (str): Specifies the application label 'accounts' to which 
                             this model belongs.
        """
        app_label = 'accounts'
