SECRET_KEY = 'local_insecure_secret_key'
DEBUG = True
ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['http://localhost:3000']

INTERNAL_IPS = [
    "127.0.0.1",  # show Django Debug Toolbar for local development
]

CORS_ORIGIN_ALLOW_ALL = True
