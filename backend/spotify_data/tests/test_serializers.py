"""
Test module for serializers in backend/spotify_data/serializers.py.
"""

import pytest
from django.contrib.auth.models import User

from backend.spotify_data.models import Song, SpotifyUser
from backend.spotify_data.serializers import (
    AlbumSerializer,
    ArtistSerializer,
    ImageSerializer,
    SongSerializer,
    SpotifyUserSerializer,
    TrackSerializer,
    UserSerializer,
)


def test_image_serializer():
    """
    Test the ImageSerializer with valid, partial, and invalid data.
    """
    # Valid data
    valid_data = {
        'url': 'https://example.com/image.jpg',
        'height': 640,
        'width': 480,
    }
    serializer = ImageSerializer(data=valid_data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data == valid_data

    # Missing optional fields
    partial_data = {'url': 'https://example.com/image.jpg'}
    serializer = ImageSerializer(data=partial_data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data['height'] is None
    assert serializer.validated_data['width'] is None

    # Invalid data
    invalid_data = {
        'url': 'not-a-valid-url',
        'height': 'not-an-integer',
        'width': 'not-an-integer',
    }
    serializer = ImageSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'url' in serializer.errors
    assert 'height' in serializer.errors
    assert 'width' in serializer.errors


def test_artist_serializer():
    """
    Test the ArtistSerializer with valid and invalid data.
    """
    valid_data = {
        'id': 'artist123',
        'name': 'Test Artist',
        'genres': ['pop', 'rock'],
        'popularity': 80,
        'images': [
            {
                'url': 'https://example.com/image1.jpg',
                'height': 640,
                'width': 480,
            },
            {'url': 'https://example.com/image2.jpg'},
        ],
    }
    serializer = ArtistSerializer(data=valid_data)
    assert serializer.is_valid(), serializer.errors
    validated_data = serializer.validated_data
    assert validated_data['id'] == 'artist123'
    assert validated_data['name'] == 'Test Artist'
    assert validated_data['genres'] == ['pop', 'rock']
    assert validated_data['popularity'] == 80
    assert len(validated_data['images']) == 2

    # Invalid data: Missing required fields
    invalid_data = {'name': 'Test Artist'}
    serializer = ArtistSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'id' in serializer.errors
    assert 'genres' in serializer.errors
    assert 'popularity' in serializer.errors


def test_album_serializer():
    """
    Test the AlbumSerializer with valid data.
    """
    valid_data = {
        'id': 'album123',
        'name': 'Test Album',
        'release_date': '2023-01-01',
        'images': [],
    }
    serializer = AlbumSerializer(data=valid_data)
    assert serializer.is_valid(), serializer.errors
    validated_data = serializer.validated_data
    assert validated_data['id'] == 'album123'
    assert validated_data['name'] == 'Test Album'
    assert validated_data['release_date'] == '2023-01-01'


def test_track_serializer():
    """
    Test the TrackSerializer with valid and invalid data.
    """
    valid_data = {
        'id': 'track123',
        'name': 'Test Track',
        'artists': [
            {
                'id': 'artist123',
                'name': 'Test Artist',
                'genres': ['pop'],
                'popularity': 80,
                'images': [],
            }
        ],
        'album': {
            'id': 'album123',
            'name': 'Test Album',
            'release_date': '2023-01-01',
            'images': [],
        },
        'duration_ms': 200000,
        'popularity': 90,
    }
    serializer = TrackSerializer(data=valid_data)
    assert serializer.is_valid(), serializer.errors
    validated_data = serializer.validated_data
    assert validated_data['id'] == 'track123'
    assert validated_data['name'] == 'Test Track'
    assert validated_data['duration_ms'] == 200000
    assert validated_data['popularity'] == 90

    # Invalid data: Missing required fields
    invalid_data = {'id': 'track123', 'name': 'Test Track'}
    serializer = TrackSerializer(data=invalid_data)
    assert not serializer.is_valid()
    assert 'artists' in serializer.errors
    assert 'album' in serializer.errors
    assert 'duration_ms' in serializer.errors
    assert 'popularity' in serializer.errors


@pytest.mark.django_db
def test_user_serializer():
    """
    Test the UserSerializer with a User instance.
    """
    user = User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        first_name='Test',
        last_name='User',
        password='password123',
    )
    serializer = UserSerializer(user)
    data = serializer.data
    assert data['username'] == 'testuser'
    assert data['email'] == 'testuser@example.com'
    assert data['first_name'] == 'Test'
    assert data['last_name'] == 'User'


@pytest.mark.django_db
def test_song_serializer():
    """
    Test the SongSerializer with a Song instance.
    """
    song = Song.objects.create(
        title='Test Song',
        artist='Test Artist',
        duration=300,
    )
    serializer = SongSerializer(song)
    data = serializer.data
    assert data['title'] == 'Test Song'
    assert data['artist'] == 'Test Artist'
    assert data['duration'] == 300

    # Test deserialization
    new_data = {
        'title': 'Another Test Song',
        'artist': 'Another Test Artist',
        'duration': 250,
    }
    serializer = SongSerializer(data=new_data)
    assert serializer.is_valid(), serializer.errors
    song = serializer.save()
    assert song.title == 'Another Test Song'
    assert song.artist == 'Another Test Artist'
    assert song.duration == 250


@pytest.mark.django_db
def test_spotify_user_serializer():
    """
    Test the SpotifyUserSerializer with a SpotifyUser instance.
    """
    user = User.objects.create_user(
        username='spotifyuser',
        email='spotifyuser@example.com',
        first_name='Spotify',
        last_name='User',
        password='password123',
    )

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
    assert data['user']['username'] == 'spotifyuser'
    assert data['favorite_tracks_short'] == []
    assert data['favorite_artists_short'] == []
    # Add more assertions as needed
