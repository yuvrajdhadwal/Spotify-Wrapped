import pytest
from django.contrib.auth.models import User
from spotify_data.models import SpotifyUser
from spotify_data.serializers import (
    ImageSerializer,
    ArtistSerializer,
    AlbumSerializer,
    TrackSerializer,
    SpotifyUserSerializer,
)


def test_image_serializer():
    """Test the ImageSerializer with valid, partial, and invalid data."""
    # Valid data
    valid_data = {
        'url': 'https://example.com/image.jpg',
        'height': 640,
        'width': 480,
    }
    serializer = ImageSerializer(data=valid_data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data == valid_data

    # Partial data (missing optional fields)
    partial_data = {'url': 'https://example.com/image.jpg'}
    serializer = ImageSerializer(data=partial_data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data['height'] is None
    assert serializer.validated_data['width'] is None

    # Invalid data
    invalid_data = {
        'url': 'invalid-url',
        'height': 'not-an-integer',
        'width': 'not-an-integer',
    }
    serializer = ImageSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'url' in serializer.errors
    assert 'height' in serializer.errors
    assert 'width' in serializer.errors


def test_artist_serializer():
    """Test the ArtistSerializer with valid and invalid data."""
    valid_data = {
        'id': 'artist123',
        'name': 'Artist Name',
        'genres': ['pop', 'rock'],
        'popularity': 85,
        'images': [
            {'url': 'https://example.com/image1.jpg', 'height': 640, 'width': 480},
            {'url': 'https://example.com/image2.jpg'},
        ],
    }
    serializer = ArtistSerializer(data=valid_data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data['id'] == 'artist123'
    assert serializer.validated_data['genres'] == ['pop', 'rock']

    # Invalid data
    invalid_data = {'name': 'Artist Without ID'}
    serializer = ArtistSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'id' in serializer.errors


def test_album_serializer():
    """Test the AlbumSerializer with valid data."""
    valid_data = {
        'id': 'album123',
        'name': 'Album Name',
        'release_date': '2024-01-01',
        'images': [],
    }
    serializer = AlbumSerializer(data=valid_data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data['id'] == 'album123'
    assert serializer.validated_data['name'] == 'Album Name'


def test_track_serializer():
    """Test the TrackSerializer with valid and invalid data."""
    valid_data = {
        'id': 'track123',
        'name': 'Track Name',
        'artists': [{'id': 'artist123', 'name': 'Artist Name', 'genres': ['pop'], 'popularity': 80, 'images': []}],
        'album': {'id': 'album123', 'name': 'Album Name', 'release_date': '2024-01-01', 'images': []},
        'duration_ms': 240000,
        'popularity': 95,
    }
    serializer = TrackSerializer(data=valid_data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data['id'] == 'track123'

    # Invalid data
    invalid_data = {'id': 'track123'}
    serializer = TrackSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'artists' in serializer.errors
    assert 'album' in serializer.errors


@pytest.mark.django_db
def test_spotify_user_serializer():
    """Test the SpotifyUserSerializer with a SpotifyUser instance."""
    user = User.objects.create_user(username='testuser', password='testpassword')
    spotify_user = SpotifyUser.objects.create(
        user=user,
        favorite_tracks_short=[],
        favorite_tracks_medium=[],
        favorite_tracks_long=[],
        favorite_artists_short=[],
        favorite_artists_medium=[],
        favorite_artists_long=[],
        favorite_genres_short=[],
        favorite_genres_medium=[],
        favorite_genres_long=[],
        quirkiest_artists_short=[],
        quirkiest_artists_medium=[],
        quirkiest_artists_long=[],
    )

    serializer = SpotifyUserSerializer(spotify_user)
    data = serializer.data
    assert data['user'] == user.id  # Check for serialized user ID
    assert data['favorite_tracks_short'] == []
    assert data['favorite_artists_short'] == []
