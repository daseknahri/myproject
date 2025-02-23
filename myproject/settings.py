"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static


USE_I18N = True  # Enable translations
USE_L10N = True  # Format numbers, dates, etc., based on the language
TIME_ZONE = 'UTC'


USE_TZ = True
TIME_ZONE = 'Africa/Casablanca'


# Default language
LANGUAGE_CODE = 'ar'

LANGUAGES = [
    ('en', 'English'),
    ('fr', 'Frencais'),
    ('ar', 'العربية'),
]

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Where translation files will be stored
LOCALE_PATHS = [
    BASE_DIR / 'locale/',  # Django will store translations here
]
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!f6nd9z0d(h9!tzj)xf6i*-o(7i1v*u*=hvvuo_rr14@q5)qc5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'unfold',
    'imagekit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rent',
]
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB in bytes

MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'twinstbcar',           # The name of your database
        'USER': 'twinstbcar',           # The database user
        'PASSWORD': '222twins',   # The database password
        'HOST': 'localhost',              # Set to 'localhost' if running locally
        'PORT': '5432',                   # Default PostgreSQL port
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

UNFOLD = {
    "SITE_TITLE": "TWINS T.B CAR",
    "SITE_HEADER": _("TWINS T.B CAR"),
    "SITE_SUBHEADER": _("Welcome to Administration"),

    "SHOW_HISTORY": True,  # Show the History button in the admin interface
    "SHOW_VIEW_ON_SITE": True,  # Show the "View on Site" button
    "SIDEBAR": {
        "navigation": [
            {
                "title": _("Control Panel"),  # Title of the section in the sidebar
                "collapsible": False,  # The section is not collapsible
                "items": [
                    {
                        "title": _("Reservations"),  # Title for the Reservation model
                        "icon": "event",  # Choose an appropriate icon (you can use any icon from Material Icons)
                        "link": reverse_lazy("admin:rent_reservation_changelist"),  # Replace 'yourapp' with your app's name
                    },
                    {
                        "title": _("Cars"),  # Title for the Car model
                        "icon": "directions_car",
                        "link": reverse_lazy("admin:rent_car_changelist"),  # Replace 'yourapp' with your app's name
                    },
                    {
                        "title": _("Clients"),  # Title for the Client model
                        "icon": "person",
                        "link": reverse_lazy("admin:rent_client_changelist"),  # Replace 'yourapp' with your app's name
                    },
                    {
                        "title": _("Payments"),  # Title for the Payment model
                        "icon": "payment",
                        "link": reverse_lazy("admin:rent_payment_changelist"),  # Replace 'yourapp' with your app's name
                    },
                    {
                        "title": _("Car Expenditures"),  # Title for the CarExpenditure model
                        "icon": "attach_money",
                        "link": reverse_lazy("admin:rent_carexpenditure_changelist"),  # Replace 'yourapp' with your app's name
                    },
                    {
                        "title": _("Business Expenditures"),  # Title for the BusinessExpenditure model
                        "icon": "business",
                        "link": reverse_lazy("admin:rent_businessexpenditure_changelist"),  # Replace 'yourapp' with your app's name
                    },
                ],
            },
        ],
    },
    "SHOW_LANGUAGES": True,
    "STYLES": [
        lambda request: static("style.css"),
    ],
    "SCRIPTS": [
        lambda request: static("mobile.js"),
    ],
}
