from functools import cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_id: str
    app_secret: str


@cache
def get_settings():
    return Settings()
