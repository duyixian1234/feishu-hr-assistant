"""Define Settings class"""

from functools import cache

from pydantic import BaseSettings


class Settings(BaseSettings):  # pylint:disable=too-few-public-methods
    """Settings for the application."""

    app_id: str
    app_secret: str
    db_url: str


@cache
def get_settings():
    """Get settings"""
    return Settings()
