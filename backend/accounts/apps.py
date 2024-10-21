"""
This module defines the configuration for the 'accounts' application in the Django project.

The `AccountsConfig` class is used by Django to configure application-specific settings,
such as the app's name and the type of auto-generated primary keys used for models.

Classes:
    - AccountsConfig: The configuration class for the 'accounts' app.

Attributes:
    - default_auto_field (str): Specifies the type of auto-generated field to use for primary keys.
    - name (str): The name of the application (in this case, 'accounts').
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    This class configures specific settings for the 'accounts' app, including the default
    type of primary key field and the app name.

    Attributes:
        default_auto_field (str): The type of primary key field to use for models by default 
                                  (BigAutoField).
        name (str): The name of the app, which is 'accounts'.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
