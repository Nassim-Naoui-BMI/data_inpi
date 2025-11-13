import os

class Config:
    DEBUG = True
    auth_url = "https://registre-national-entreprises.inpi.fr/api/sso/login"
    api_url = "https://registre-national-entreprises.inpi.fr/api/companies"
    username = os.environ.get("INPI_CLIENT_ID")
    password = os.environ.get("INPI_CLIENT_SECRET")
