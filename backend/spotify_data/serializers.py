# backend/spotify_data/serializers.py

"""
Serializers for Spotify Roasted models.
"""

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Song, SpotifyUser

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the Django User model.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ImageSerializer(serializers.Serializer):
    """
    Serializer for image data in artist profiles.
    """
    url = serializers.URLField()
    height = serializers.IntegerField(required=False, allow_null=True)
    width = serializers.IntegerField(required=False, allow_null=True)

class ArtistSerializer(serializers.Serializer):
    """
    Serializer for artist data stored in JSONFields.
    """
    id = serializers.CharField()
    name = serializers.CharField()
    genres = serializers.ListField(child=serializers.CharField())
    popularity = serializers.IntegerField()
    images = ImageSerializer(many=True, required=False)

class AlbumSerializer(serializers.Serializer):
    """
    Serializer for album data in track information.
    """
    id = serializers.CharField()
    name = serializers.CharField()
    release_date = serializers.CharField()
    images = ImageSerializer(many=True, required=False)

class TrackSerializer(serializers.Serializer):
    """
    Serializer for track data stored in JSONFields.
    """
    id = serializers.CharField()
    name = serializers.CharField()
    artists = ArtistSerializer(many=True)
    album = AlbumSerializer()
    duration_ms = serializers.IntegerField()
    popularity = serializers.IntegerField()

class SpotifyUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the SpotifyUser model, including nested user data
    and expanded JSONFields.
    """
    user = UserSerializer(read_only=True)
    favorite_tracks_short = TrackSerializer(many=True)
    favorite_tracks_medium = TrackSerializer(many=True)
    favorite_tracks_long = TrackSerializer(many=True)
    favorite_artists_short = ArtistSerializer(many=True)
    favorite_artists_medium = ArtistSerializer(many=True)
    favorite_artists_long = ArtistSerializer(many=True)
    favorite_genres_short = serializers.ListField(child=serializers.CharField())
    favorite_genres_medium = serializers.ListField(child=serializers.CharField())
    favorite_genres_long = serializers.ListField(child=serializers.CharField())
    quirkiest_artists_short = ArtistSerializer(many=True)
    quirkiest_artists_medium = ArtistSerializer(many=True)
    quirkiest_artists_long = ArtistSerializer(many=True)

    class Meta:
        model = SpotifyUser
        fields = '__all__'
