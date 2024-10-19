from django.db import models

# Create your models here.
"""
What is stored in our database for every single spotify token
The important thing is we store when every token expires so we know if a current user token is in
need of refreshing
"""
class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)