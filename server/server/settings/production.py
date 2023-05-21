import os

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False

# allow production reverse proxy to work
ALLOWED_HOSTS = ['localhost']
CORS_ALLOWED_ORIGINS = ['http://localhost']
