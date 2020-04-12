from .base import *
import os

# INSTALLED_APPS += [
#     'corsheaders',
# ]

# MIDDLEWARE = [  # Or MIDDLEWARE_CLASSES on Django < 1.10
#     'corsheaders.middleware.CorsMiddleware',
# ] + MIDDLEWARE


# CORS_ORIGIN_ALLOW_ALL = True

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = 'https://storage.yandexcloud.net'
AWS_S3_REGION_NAME = 'ru-central1'
AWS_DEFAULT_ACL = None

# AWS_S3_CUSTOM_DOMAIN = f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# static settings - using local
# STATIC_LOCATION = 'static'
# STATIC_URL = f'{AWS_S3_ENDPOINT_URL}/{STATIC_LOCATION}/'
# STATICFILES_STORAGE = 'cmux_project.storage_backends.StaticStorage'
# s3 public media settings
PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{PUBLIC_MEDIA_LOCATION}/'
DEFAULT_FILE_STORAGE = 'cmux_project.storage_backends.PublicMediaStorage'
# s3 private media settings
PRIVATE_MEDIA_LOCATION = 'private'
PRIVATE_FILE_STORAGE = 'cmux_project.storage_backends.PrivateMediaStorage'
