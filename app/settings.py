"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from os import (
    environ,
    path,
)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

# Environment
DJANGO_ENV = environ['DJANGO_ENV']
DJANGO_ENV_PROD = 'prod'
DJANGO_ENV_DEV = 'dev'

# Usable settings constant
DJANGO_ENV_IS_PROD = DJANGO_ENV == DJANGO_ENV_PROD

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = environ['DJANGO_SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
if DJANGO_ENV == DJANGO_ENV_PROD:
    DEBUG = False
elif DJANGO_ENV == DJANGO_ENV_DEV:
    DEBUG = True

if DJANGO_ENV == DJANGO_ENV_PROD:
    ALLOWED_HOSTS = [
        'api.billshare.io',
        'billshare.io',
        'localhost',
        'localhost:3000',
        '127.0.0.1',
        '127.0.0.1:3000',
    ]
elif DJANGO_ENV == DJANGO_ENV_DEV:
    ALLOWED_HOSTS = [
        'localhost',
        'localhost:3000',
        '127.0.0.1',
        '127.0.0.1:3000',
    ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'corsheaders',
    'djmoney',
    'app.group',
    'app.transaction',
    'app.user',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'app.urls'

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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ['DATABASE_NAME'],
        'USER': environ['DATABASE_USER'],
        'PASSWORD': environ['DATABASE_PASSWORD'],
        'HOST': environ['DATABASE_HOST'],
        'PORT': environ['DATABASE_PORT'],
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = environ['EMAIL_HOST']
EMAIL_PORT = environ['EMAIL_PORT']
EMAIL_HOST_USER = environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = environ['EMAIL_HOST_PASSWORD']

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Custom Settings
SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = 'DENY'

PREPEND_WWW = False

# For SEO reasons, choose one or the other
APPEND_SLASH = True

# SSL Settings
SESSION_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = False
SECURE_SSL_REDIRECT = False

# Setup Custom Auth User
AUTH_USER_MODEL = 'user.User'

# Cors Middleware
CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = ALLOWED_HOSTS
CORS_ALLOW_CREDENTIALS = True

# CSRF Middleware
CSRF_TRUSTED_ORIGINS = ALLOWED_HOSTS

# TODO fix this CORS HTTP ISSUES - When moving to full HTTPS relook over these
SESSION_COOKIE_DOMAIN = '.billshare.io'
CSRF_COOKIE_DOMAIN = '.billshare.io'
