"""
Django settings for InvenTree project.

In practice the settings in this file should not be adjusted,
instead settings can be configured in the config.yaml file
located in the top level project directory.

This allows implementation configuration to be hidden from source control,
as well as separate configuration parameters from the more complex
database setup in this file.

"""

import os
import logging
import tempfile
import yaml

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

cfg_filename = os.path.join(BASE_DIR, 'config.yaml')

if not os.path.exists(cfg_filename):
    CONFIG = {}
    print("Warning: config.yaml not found - using default settings")
else:
    with open(cfg_filename, 'r') as cfg:
        CONFIG = yaml.safe_load(cfg)

# Read the autogenerated key-file
key_file = open(os.path.join(BASE_DIR, 'secret_key.txt'), 'r')

SECRET_KEY = key_file.read().strip()

# Default action is to run the system in Debug mode
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.get('debug', True)

# List of allowed hosts (default = allow all)
ALLOWED_HOSTS = CONFIG.get('allowed_hosts', ['*'])

# Cross Origin Resource Sharing (CORS) options

# Only allow CORS access to API
CORS_URLS_REGEX = r'^/api/.*$'

# Extract CORS options from configuration file
cors_opt = CONFIG.get('cors', None)

if cors_opt:
    CORS_ORIGIN_ALLOW_ALL = cors_opt.get('allow_all', False)

    if CORS_ORIGIN_ALLOW_ALL:
        print("Warning: CORS requests are allowed for any domain!")
    else:
        CORS_ORIGIN_WHITELIST = cors_opt.get('whitelist', [])

if DEBUG:
    # will output to your console
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
    )

# Application definition

INSTALLED_APPS = [

    # Core django modules
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # InvenTree apps
    'part.apps.PartConfig',
    'stock.apps.StockConfig',
    'company.apps.CompanyConfig',
    'build.apps.BuildConfig',
    'order.apps.OrderConfig',

    # Third part add-ons
    'django_filters',               # Extended filter functionality
    'dbbackup',                     # Database backup / restore
    'rest_framework',               # DRF (Django Rest Framework)
    'rest_framework.authtoken',     # Token authentication for API
    'corsheaders',                  # Cross-origin Resource Sharing for DRF
    'crispy_forms',                 # Improved form rendering
    'import_export',                # Import / export tables to file
    'django_cleanup',               # Automatically delete orphaned MEDIA files
    'qr_code',                      # Generate QR codes
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'InvenTree.middleware.AuthRequiredMiddleware',
]

if CONFIG.get('log_queries', False):
    MIDDLEWARE.append('InvenTree.middleware.QueryCountMiddleware')

ROOT_URLCONF = 'InvenTree.urls'

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
            ],
        },
    },
]

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

WSGI_APPLICATION = 'InvenTree.wsgi.application'

DATABASES = {}

# Database backend selection
if 'database' in CONFIG:
    DATABASES['default'] = CONFIG['database']
else:
    print("Warning: Database backend not specified - using default (sqlite)")
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'inventree_db.sqlite3'),
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'qr-code': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'qr-code-cache',
        'TIMEOUT': 3600
    }
}

QR_CODE_CACHE_ALIAS = 'qr-code'

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = CONFIG.get('static_root', os.path.join(BASE_DIR, 'static'))

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'InvenTree', 'static'),
]

MEDIA_URL = '/media/'

MEDIA_ROOT = CONFIG.get('media_root', os.path.join(BASE_DIR, 'media'))

# crispy forms use the bootstrap templates
CRISPY_TEMPLATE_PACK = 'bootstrap'

# Use database transactions when importing / exporting data
IMPORT_EXPORT_USE_TRANSACTIONS = True

# Settings for dbbsettings app
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {
    'location': CONFIG.get('backup_dir', tempfile.gettempdir()),
}
