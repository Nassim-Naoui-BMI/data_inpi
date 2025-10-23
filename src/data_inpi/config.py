import os


class Config:
    DEBUG = True
    auth_url = os.environ.get("INPI_AUTH_URL")
    api_url = os.environ.get("INPI_API_URL")
    username = os.environ.get("INPI_CLIENT_ID")
    password = os.environ.get("INPI_CLIENT_SECRET")
