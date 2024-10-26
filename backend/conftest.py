"""
Test configuration and fixtures for the Django project.

This `conftest.py` file sets up the testing environment for the Django project, 
configuring essential settings and providing reusable fixtures for test cases. 
It handles Django initialization and provides commonly used test resources, 
such as a test client and a test user.

Fixtures:
    - client: Provides a Django test client instance for simulating HTTP requests.
    - test_user: Creates and returns a test user instance in the test database.

Functions:
    - pytest_configure: Configures the Django settings for pytest, initializing 
      the Django environment and allowing for ORM and app registry usage within tests.

This setup helps to ensure consistency and reliability in test runs, making it 
easier to write, maintain, and execute Django tests across the project.
"""
import os
import sys

# Calculate the absolute path to the 'backend' directory
backend_path = os.path.abspath(os.path.dirname(__file__))

# Add 'backend' to sys.path if it's not already there
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

print("sys.path:", sys.path)  # For debugging


import pytest
import django


def pytest_configure():
    """
    Configures the Django settings for pytest.

    Sets up the Django environment by specifying the settings 
    module (`DJANGO_SETTINGS_MODULE`) and calling `django.setup()`. This is 
    necessary for Django ORM and app registry to function correctly in tests.

    If the `DJANGO_SETTINGS_MODULE` environment variable is not already set, 
    it will default to `'spotify_wrapper.settings'`.

    Returns:
        None
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spotify_wrapper.settings')
    django.setup()


@pytest.fixture
def client():
    """
    Provides a Django test client instance for making requests in tests.

    The client fixture allows for simulating HTTP requests in tests, enabling 
    testing of views and middleware without needing a running server. It is 
    only imported after Django setup to avoid dependency issues.

    Yields:
        django.test.Client: A Django test client instance.
    """
    from django.test import Client  # Import Client only after Django setup
    return Client()

@pytest.fixture
def test_user(db):
    """
    Creates and returns a test user instance in the database.

    This fixture creates a test user using Django's `User` model, which can 
    then be used in tests where an authenticated or existing user is required. 
    It requires the `db` fixture to ensure the test database is set up and 
    ready for database operations.

    Args:
        db: A fixture provided by pytest-django to manage database setup.

    Returns:
        User: A Django user instance created for testing purposes.
    """
    from django.contrib.auth.models import User  # Import User after Django setup
    user = User.objects.create(username="testuser")
    return user
