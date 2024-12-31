"""
Django settings for awmca2 project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import dj_database_url
import django_heroku
import os


from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

CORS_ALLOW_HEADERS = default_headers + (

    'Access-Control-Allow-Origin',

)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-=&h^@av&#a%n=4la-o5)tm%@(_x1-hv%z*+c11k#@^#01+c=x1"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

#ALLOWED_HOSTS = []
#ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'localhost']
ALLOWED_HOSTS = ['gas-station-finder-app-80f702109b4d.herokuapp.com', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pwa',
    'myapp',
    'rest_framework',
    'leaflet',
    'corsheaders',
    'frontend',
]

# Configure PWA settings
PWA_APP_NAME = 'WebMap'
PWA_APP_DESCRIPTION = "A Progressive Web Application for WebMap"
PWA_APP_THEME_COLOR = '#000000'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_START_URL = '/'
PWA_APP_ICONS = [
    {
        'src': '/static/images/icons/icon-72x72.png',
        'sizes': '72x72',
    },
    {
        'src': '/static/images/icons/icon-96x96.png',
        'sizes': '96x96',
    },
    {
        'src': '/static/images/icons/icon-128x128.png',
        'sizes': '128x128',
    },
    {
        'src': '/static/images/icons/icon-144x144.png',
        'sizes': '144x144',
    },
    {
        'src': '/static/images/icons/icon-152x152.png',
        'sizes': '152x152',
    },
    {
        'src': '/static/images/icons/icon-192x192.png',
        'sizes': '192x192',
    },
    {
        'src': '/static/images/icons/icon-384x384.png',
        'sizes': '384x384',
    },
    {
        'src': '/static/images/icons/icon-512x512.png',
        'sizes': '512x512',
    },
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/images/icons/icon-152x152.png',
        'sizes': '152x152',
    },
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/icons/splash-640x1136.png',
        'media': '(device-width: 320px) and (device-height: 568px)',
    },
    {
        'src': '/static/images/icons/splash-750x1334.png',
        'media': '(device-width: 375px) and (device-height: 667px)',
    },
    {
        'src': '/static/images/icons/splash-828x1792.png',
        'media': '(device-width: 414px) and (device-height: 896px)',
    },
    {
        'src': '/static/images/icons/splash-1125x2436.png',
        'media': '(device-width: 375px) and (device-height: 812px)',
    },
    {
        'src': '/static/images/icons/splash-1242x2208.png',
        'media': '(device-width: 414px) and (device-height: 736px)',
    },
    {
        'src': '/static/images/icons/splash-1242x2688.png',
        'media': '(device-width: 414px) and (device-height: 896px)',
    },
    {
        'src': '/static/images/icons/splash-1536x2048.png',
        'media': '(device-width: 768px) and (device-height: 1024px)',
    },
    {
        'src': '/static/images/icons/splash-1668x2224.png',
        'media': '(device-width: 834px) and (device-height: 1112px)',
    },
    {
        'src': '/static/images/icons/splash-1668x2388.png',
        'media': '(device-width: 834px) and (device-height: 1194px)',
    },
    {
        'src': '/static/images/icons/splash-2048x2732.png',
        'media': '(device-width: 1024px) and (device-height: 1366px)',
    },
]

PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'


LEAFLET_CONFIG = {
    # "SPATIAL_EXTENT": (5.0, 44.0, 7.5, 46),
    "DEFAULT_CENTER": (13.3888599, 52.5170365), #set your corordinate to reference to a solid place (the above coordinates places you somewhere on the sea in the middle east )
    "DEFAULT_ZOOM": 16,
    "MIN_ZOOM": 3,
    "MAX_ZOOM": 20,
    "DEFAULT_PRECISION": 6,
    "SCALE": "both",
    "ATTRIBUTION_PREFIX": "powered by <Your corporate name>",
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
]

ROOT_URLCONF = "awmca2.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / 'templates',
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "awmca2.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',  # Use PostGIS
#         'NAME': 'gas_station_database',
#         'USER': 'postgres',  # replace with your PostgreSQL username
#         'PASSWORD': 'password',  # replace with your PostgreSQL password
#         'HOST': 'localhost',  # or the appropriate host
#         'PORT': '5432',  # default PostgreSQL port
#     }
# }

# DATABASES = {
#      'default': dj_database_url.config(
#          default='postgres://uaodt6ro3jmkqu:p747066a598e26f9a65cbb4621adfa35892aa9604323c84fa1e2c9a21586473f4@c3l5o0rb2a6o4l.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com:5432/d6toit0l00v9qc', conn_max_age=600, ssl_require=True)
#  }

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',  # Use PostGIS
        'NAME': 'd6toit0l00v9qc',  # Database name
        'USER': 'uaodt6ro3jmkqu',  # Username
        'PASSWORD': 'p747066a598e26f9a65cbb4621adfa35892aa9604323c84fa1e2c9a21586473f4',  # Password
        'HOST': 'c3l5o0rb2a6o4l.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com',  # Host
        'PORT': '5432',  # Port
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"


# STATIC_URL = '/static/'

# In production, you will need to configure your static files to be served properly.
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Ensure Django knows where to look for static files
]
STATIC_ROOT = BASE_DIR / "staticfiles"  # Directory to collect static files

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# GDAL library path
import os
#GDAL_LIBRARY_PATH = r'C:\Users\Nazil\anaconda3\envs\awm_env\Library\bin\gdal.dll'
GDAL_LIBRARY_PATH = os.getenv('GDAL_LIBRARY_PATH', r'C:\Users\Nazil\anaconda3\envs\awm_env\Library\bin\gdal.dll')
GEOS_LIBRARY_PATH = r'C:\Users\Nazil\anaconda3\envs\awm_env\Library\bin\geos_c.dll'



CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [

    'http://localhost:80',

    'http://localhost:8000',

    'http://127.0.0.1:8000' , 

    'https://gas-station-finder-app-80f702109b4d.herokuapp.com'

]


# This is for login 
# Add authentication configuration
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = '/'  # Redirect to home after logout
LOGIN_REDIRECT_URL = '/'   # Redirect to home after login

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


django_heroku.settings(locals())
