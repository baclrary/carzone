import dj_database_url

from os import getenv

DEBUG = False

DATABASES = {'default': dj_database_url.config(default=getenv("DATABASE_STR"))}

# EMAIL
EMAIL_BACKEND = getenv("EMAIL_BACKEND")
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = getenv("EMAIL_PORT")
EMAIL_HOST_USER = getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = getenv("EMAIL_HOST_PASSWORD")
