"""
Django settings for tquarters project.

Generated by 'django-admin startproject' using Django 3.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import django_heroku
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y7rjkta3a83&&7(rocf0bj!!=5$i(1wrt25ewoua0k6dy8%snr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'django.contrib.sites',

    'accounts',
    'shared',
    'product',
    'checkout',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'shared.middleware.CheckEmailValidatedMiddleware',
]

ROOT_URLCONF = 'tquarters.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'shared.context.base_context',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

WSGI_APPLICATION = 'tquarters.wsgi.application'

SITE_ID = 2

FROM_EMAIL = 'kumarpulkit35@gmail.com'
ADMIN_EMAIL = 'kboama@live.com'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

LOGIN_REDIRECT_URL = "/"
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'
DEFAULT_FROM_EMAIL = 'kumarpulkit35@gmail.com'
DEFAULT_CONTACT_EMAIL = 'kumarpulkit35@gmail.com'

SENDGRID_KEY = ''

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'kumarpulkit35@gmail.com'
EMAIL_HOST_PASSWORD = 'pvjetotxdspitqan'

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION  = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_UNIQUE_EMAIL = True
EMAIL_CONFIRMATION_SIGNUP = True

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5

AUTH_USER_MODEL = 'accounts.User'
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd9jnrcr9fb990r',
        'USER': 'wqzluapdriaehz',
        'PASSWORD': '15df0e34ca6b33dd8f0044224fa1652f825dab1e1d89b0476befe27862e41e8b',
        'HOST': 'ec2-44-209-57-4.compute-1.amazonaws.com',
        'PORT': '5432'
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'tquarters',
#         'USER': 'postgres',
#         'PASSWORD': 'postgres',
#         'HOST': 'localhost',
#         'PORT': '5432'
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfile')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
django_heroku.settings(locals())

MEDIA_URL = '/media/'

# stripe
# STRIPE_KEYS = {
#     'API_KEY': 'sk_live_QNgbPdHggWGiDyMcmtuf15aX',
#     'PUBLIC_KEY': 'pk_live_QkGIiG8xGX2NVoHrHMXq9qJQ',
#     'CLIENT_ID': 'ca_CVXrWuRzBwmRpDDewbv7wuvGuMQ33EU6',
# }

STRIPE_KEYS = {
    'API_KEY': 'sk_test_xUJYrgdKRvvpZuKscPUdLxx9',
    'PUBLIC_KEY': 'pk_test_KNGdSFkU1ZNY7jzTfHds62BD',
    'CLIENT_ID': 'ca_CVXrhXIJ2jCQxtBNp6266hKc0rTPtegW',
}

STRIPE_PUBLISH_KEY = "pk_test_KNGdSFkU1ZNY7jzTfHds62BD"


try:
    from .settings_local import *
except:
    pass

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

# BASE_URL = 'http://127.0.0.1:8000'
BASE_URL = 'https://tquarters-app.herokuapp.com'
