"""
Serializers for Spotify Roasted models.
"""

from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Song, SpotifyUser, SpotifyWrapped, DuoWrapped

class SongSerializer(serializers.ModelSerializer):
    """
    Serializer for Song model.
    """
    class Meta: # pylint: disable=too-few-public-methods
        """
        meta class
        """
        model = Song
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the Django User model.
    """
    class Meta: # pylint: disable=too-few-public-methods
        """
        meta class
        """
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ImageSerializer(serializers.Serializer): # pylint: disable=abstract-method
    """
    Serializer for image data in artist profiles.
    """
    url = serializers.URLField()
    height = serializers.IntegerField(required=False, allow_null=True, default=None)
    width = serializers.IntegerField(required=False, allow_null=True, default=None)

class ArtistSerializer(serializers.Serializer): # pylint: disable=abstract-method
    """
    Serializer for artist data stored in JSONFields.
    """
    id = serializers.CharField()
    name = serializers.CharField()
    genres = serializers.ListField(required=False)
    popularity = serializers.IntegerField(required=False)
    images = ImageSerializer(many=True, required=False)


class AlbumSerializer(serializers.Serializer): # pylint: disable=abstract-method
    """
    Serializer for album data in track information.
    """
    id = serializers.CharField()
    name = serializers.CharField()
    release_date = serializers.CharField()
    images = ImageSerializer(many=True, required=False)

class TrackSerializer(serializers.Serializer): # pylint: disable=abstract-method
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
    # user = UserSerializer(read_only=True)
    # favorite_tracks_short = TrackSerializer(many=True)
    # favorite_tracks_medium = TrackSerializer(many=True)
    # favorite_tracks_long = TrackSerializer(many=True)
    # favorite_artists_short = ArtistSerializer(many=True)
    # favorite_artists_medium = ArtistSerializer(many=True)
    # favorite_artists_long = ArtistSerializer(many=True)
    # favorite_genres_short = serializers.ListField(child=serializers.CharField())
    # favorite_genres_medium = serializers.ListField(child=serializers.CharField())
    # favorite_genres_long = serializers.ListField(child=serializers.CharField())
    # quirkiest_artists_short = ArtistSerializer(many=True)
    # quirkiest_artists_medium = ArtistSerializer(many=True)
    # quirkiest_artists_long = ArtistSerializer(many=True)

    class Meta: # pylint: disable=too-few-public-methods
        """
        meta class
        """
        model = SpotifyUser
        fields = '__all__'

class SpotifyWrappedSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyWrapped
        fields = '__all__'


class DuoWrappedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DuoWrapped
        fields = '__all__'
