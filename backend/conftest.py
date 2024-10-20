import pytest
import django
from django.conf import settings
import os

def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spotify_wrapper.settings')  # Update if necessary
    django.setup()


@pytest.fixture
def client():
    from django.test import Client  # Import Client only after Django setup
    return Client()

@pytest.fixture
def test_user(db):
    from django.contrib.auth.models import User  # Import User after Django setup
    user = User.objects.create(username="testuser")
    return user
