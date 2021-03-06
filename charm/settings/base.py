"""
Django settings for charm project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    # These are our custom written apps.
    'charm.core',
    'charm.colorfield',
    'charm.api',
    'charm.home',
    'charm.reports',
    'charm.user',
    'charm.coach',
    'charm.registration',
    'charm.customer',
    'charm.beautyreport',
    'charm.anamnese',
    'charm.questionnaire',

    # Graphene-Django is built on top of Graphene and is needed for GraphQL (charm.api dependency)
    # https://docs.graphene-python.org/projects/django/en/latest/
    'graphene_django',

    # With the modeladmin module, we can add our models to the Wagtail admin page.
    # http://docs.wagtail.io/en/v2.6.1/reference/contrib/modeladmin/
    'wagtail.contrib.modeladmin',

    # Default Wagtail apps
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',

    # django-modelcluster extends Django's foreign key relations. It introduces a new type of relation, ParentalKey.
    # https://github.com/wagtail/django-modelcluster
    'modelcluster',
    # Django module for Tags, extending modelcluster
    'taggit',
    'corsheaders',
    'wagtailfontawesome',

    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # This is also required for GraphiQL
]

MIDDLEWARE = [
    # This middlewear is needed for configuring CORS (Cross-Origin Resource Sharing)
    'corsheaders.middleware.CorsMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',

    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

# If True, the whitelist will not be used and all origins will be accepted
# See https://pypi.org/project/django-cors-headers/
CORS_ORIGIN_ALLOW_ALL = True

# This is the Schema Graphene is using
GRAPHENE = {
    'SCHEMA': 'charm.api.schema.schema',

    # Authentication will make use of JSON Web Tokens (JWT)
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ]
}

GRAPHQL_JWT = {
    # Allow per-argument authentication system
    'JWT_ALLOW_ARGUMENT': True,
}

GRAPHQL_API = {
    'APPS': [
        'user',
        'home',
        'reports',
        'anamnese',
        'questionnaire',
        'beautyreport',
        'registration',
    ],
    'PREFIX': {
    },
    'URL_PREFIX': {
    },
    'RELAY': False,
}


AN_DOCUMENT_PATH = "media/anamneses/"
BR_DOCUMENT_PATH = "media/beautyreports/"

# JWT as authentication backend
AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Root URL path 
ROOT_URLCONF = 'charm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # os.path.join(PROJECT_DIR, 'templates'),
        ],
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
    {
        # Jinja2 is a more developer-friendly templating language based on DTL (Django Template Language)
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(PROJECT_DIR, 'jinja2'),
        ],
        'OPTIONS': {
            'extensions': [
                'wagtail.core.jinja2tags.core',
                'wagtail.admin.jinja2tags.userbar',
                'wagtail.images.jinja2tags.images',
            ],
        },
    }
]

WSGI_APPLICATION = 'charm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# The main User Model Wagtail should use
AUTH_USER_MODEL = 'user.User'


# Validators used to check if the password is secure
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Adjusted timezone
TIME_ZONE = 'Europe/Vienna'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'static'),
]

# ManifestStaticFilesStorage is recommended in production, to prevent outdated
# Javascript / CSS assets being served from cache (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/2.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 20000

# Wagtail settings

WAGTAIL_SITE_NAME = "charm"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = 'http://manage.pharmaziegasse.at'