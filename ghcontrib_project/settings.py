# -*- coding: utf-8 -*-
"""Django settings for GithubContrib project."""

import os
import os.path as op
import sys

import raven

try:
    import local_settings
except ImportError:
    try:
        from . import initial_settings as local_settings
    except ImportError:  # pragma: no cover
        print('No initial settings!')
        sys.exit()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Debugging
DEBUG = local_settings.DEBUG
INTERNAL_IPS = local_settings.INTERNAL_IPS

DATABASES = local_settings.DATABASES
WSGI_APPLICATION = 'ghcontrib_project.wsgi.application'
ROOT_URLCONF = 'ghcontrib_project.urls'
SECRET_KEY = local_settings.SECRET_KEY
ALLOWED_HOSTS = [local_settings.PROJECT_DOMAIN]
SESSION_SAVE_EVERY_REQUEST = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Custom
    'raven.contrib.django.raven_compat',
    'admin_reorder',
    'rosetta',
    'google_analytics',
    'social_django',
    'menu',
    'ghcontrib',
]
if DEBUG:  # pragma: no cover
    INSTALLED_APPS += [
        'debug_toolbar',
        'template_timings_panel',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]
if DEBUG:  # pragma: no cover
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

# Logging
if not DEBUG:  # pragma: no cover
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': ('%(levelname)s %(asctime)s %(module)s '
                           '%(process)d %(thread)d %(message)s')
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                'tags': {
                    'custom-tag': 'x'
                },
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (os.path.join(BASE_DIR, 'templates'), ),
        'OPTIONS': {
            'context_processors': (
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Custom
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                # social_django
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                # GHContrib
                'ghcontrib.context_processors.variables',
            ),
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
            'debug':
            DEBUG
        },
    },
]
if DEBUG:  # pragma: no cover
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ]

# Static files
STATIC_ROOT = op.join(local_settings.PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = op.join(local_settings.PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

# Authentification
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
AUTH_USER_MODEL = 'ghcontrib.User'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # Custom
    'social_core.backends.github.GithubOAuth2',
)

# Internationalization
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True
LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Русский'),
)
LOCALE_PATHS = (op.join(local_settings.PROJECT_ROOT, 'project', 'locale'), )

# Timezone
TIME_ZONE = 'US/Eastern'
USE_TZ = True

# Login
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# --== Modules settings ==--
# django-google-analytics-app
GOOGLE_ANALYTICS = {
    'google_analytics_id': local_settings.GOOGLE_ANALYTICS_ID,
}

# django-modeladmin-reorder
ADMIN_REORDER = (
    {
        'app': 'ghcontrib',
        'models': ('ghcontrib.User', 'ghcontrib.Repo', 'ghcontrib.Commit')
    },
    {
        'app': 'social_django',
        'models': ('social_django.UserSocialAuth', )
    },
)

# raven
RAVEN_CONFIG = {
    'dsn': local_settings.RAVEN_DSN,
    'release': raven.fetch_git_sha(local_settings.GIT_ROOT),
}

# django-debug-toolbar
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
    # django-debug-toolbar-template-timings
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
]

# social-auth-app-django

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    'social_core.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    'social_core.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    'social_core.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social_core.pipeline.social_auth.social_user',

    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    'social_core.pipeline.user.get_username',

    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    # 'social_core.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social_core.pipeline.user.create_user',

    # Create the record that associates the social account with the user.
    'social_core.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    'social_core.pipeline.social_auth.load_extra_data',

    # We might want to enable it
    # # Update the user record with any changed info from the auth service.
    # 'social_core.pipeline.user.user_details',

    # Custom
    # We do this only if the user get's created for the first time.
    'ghcontrib.social.load_user_data',
)
SOCIAL_AUTH_GITHUB_KEY = local_settings.SOCIAL_AUTH_GITHUB_KEY
SOCIAL_AUTH_GITHUB_SECRET = local_settings.SOCIAL_AUTH_GITHUB_SECRET

# --== Project settings ==--

ADMIN_EMAIL = local_settings.ADMIN_EMAIL

# API Keys
GITHUB_API_KEY = local_settings.GITHUB_API_KEY

# This is here to fix the problem with static files on dev
try:
    from local_settings2 import *  # noqa pylint: disable=wildcard-import
except ImportError:
    pass
