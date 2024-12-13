"""
Django settings for project_altaviz project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os, sys
# sys.path.append(os.path.expanduser("~"))
try:
    from .myCredentials import credentials
    # print(f'credentials from server home dir:: {credentials}')
except ImportError as e:
    print(f"Error importing credentials: {e}")
# print(f'credentials from server home dir:: {credentials}')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('MY_SECRET_KEY') if os.environ.get('MY_SECRET_KEY') else credentials['MY_SECRET_KEY'],

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = [
    # 'dafetite.pythonanywhere.com',
    'altavizapp.pythonanywhere.com',
    'altaviz-frontend.vercel.app/',
    'localhost',
    '127.0.0.1',
]
# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_sse_notification',		# <- added startapp here
    'app_deliveries',		# <- added startapp here
    'app_search',		# <- added startapp here
    'app_auth',		# <- added startapp here
    'app_custodian',		# <- added startapp here
    'app_location',		# <- added startapp here
    'app_inventory',		# <- added startapp here
    'app_bank',		# <- added startapp here
    'app_fault',		# <- added startapp here
    'app_products',		# <- added startapp here
    'app_contactus',		# <- added startapp here
    'app_users',		# <- added startapp here
    'app_altaviz',		# <- added startapp here
    'django_extensions',		# <- added django_extensions here
    'rest_framework',
    'corsheaders',
    'channels',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'project_altaviz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project_altaviz.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# print('MY_LOCAL_MACHINE:', os.environ.get('MY_LOCAL_MACHINE'))
if os.environ.get('MY_LOCAL_MACHINE'):
    # print(f"development mode: {os.environ.get('MY_LOCAL_MACHINE')}")
    # print(f"MY_LOCAL_REDIS_LOCATION (from env): {os.environ.get('MY_LOCAL_REDIS_LOCATION')}")
    # print(f"MY_LOCAL_REDIS_LOCATION (from file): {credentials['MY_LOCAL_REDIS_LOCATION']}"),
    # print(f"MY_REDIS_LOCATION (from file): {credentials['MY_REDIS_LOCATION']}"),
    DEBUG = True # for development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    # CACHES = {
    #     "default": {
    #         "BACKEND": "django_redis.cache.RedisCache",
    #         "LOCATION": credentials['MY_LOCAL_REDIS_LOCATION'],
    #         "OPTIONS": {
    #             "CLIENT_CLASS": "django_redis.client.DefaultClient",
    #         }
    #     }
    # }
    # CACHES = {
    #     "default": {
    #         "BACKEND": "django_redis.cache.RedisCache",
    #         "LOCATION": credentials['MY_REDIS_LOCATION'],
    #         "OPTIONS": {
    #             "CLIENT_CLASS": credentials['CLIENT_CLASS'],
    #             "PASSWORD": credentials['PASSWORD'],
    #         }
    #     }
    # }

else:
    DEBUG = False # production
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': credentials['MY_DB_NAME'],
            'USER': credentials['MY_DB_USERNAME'],
            'PASSWORD': credentials['MY_DB_PASSWORD'],
            'HOST': credentials['MY_DB_HOST'],
        }
    }
    # CACHES = {
    #     "default": {
    #         "BACKEND": "django_redis.cache.RedisCache",
    #         "LOCATION": credentials['MY_LOCAL_REDIS_LOCATION'],
    #         "OPTIONS": {
    #             "CLIENT_CLASS": "django_redis.client.DefaultClient",
    #         }
    #     }
    # }
    # CACHES = {
    #     "default": {
    #         "BACKEND": "django_redis.cache.RedisCache",
    #         "LOCATION": credentials['MY_REDIS_LOCATION'],
    #         "OPTIONS": {
    #             "CLIENT_CLASS": credentials['CLIENT_CLASS'],
    #             "PASSWORD": credentials['PASSWORD'],
    #         }
    #     }
    # }

# ############### for tests ##############
# DEBUG = True # for test
# SERVE_STATIC_FILES = True  # for test
# ALLOWED_HOSTS = ['*'] # for test
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'read_default_file': '../MySQL_credentials.cnf',
#         },
#     }
# }
# ########################################


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Allow credentials (cookies, authorization headers, etc.)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
# CSRF_TRUSTED_ORIGINS = ['*']
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
# ]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
# CORS_ALLOW_HEADERS = ['*']
# CORS_ALLOW_METHODS = ['*']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_ROOT = BASE_DIR / 'staticfiles'
# Added static variable here
# STATICFILES_DIRS = [
#     BASE_DIR / 'static',		# <- added static to BASE_DIR
#     BASE_DIR / 'static/article_hive_project',		# <- added static to project dir.
# ]

AUTH_USER_MODEL = 'app_users.User'

ASGI_APPLICATION = "project_altaviz.asgi.application"
# Use Django's in-memory channel layer for development
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",  # In-memory backend for development
    },
}

# Optional: Enable compression and caching for better performance
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# spin up local server:
#  daphne -p 8000 project_altaviz.asgi:application

# logon local server to test it
# websocat ws://127.0.0.1:8000/ws/notifications/
