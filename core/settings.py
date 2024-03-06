from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
import os, environ
env = environ.Env(
    DJANGO_LOG_LEVEL=(str, 'DEBUG'),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hc0@t%yva8y!z$_dlo*#lhj4-gywy!q-)x@gz7a6g19-u9(5z)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'ipays',  # new
    'channels',  # new
    'oauth2_provider',
    'corsheaders',
]
WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'  # new
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 30  # Max 30MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240   # higher than the count of fields

SESSION_EXPIRE_AT_BROWSER_CLOSE = True     # opional, as this will log you out when browser is closed
SESSION_COOKIE_AGE = 240 * 60                   # 0r 5 * 60, same thing
SESSION_SAVE_EVERY_REQUEST = True          # Will prrevent from logging you out after 300 seconds
LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_L10N = True

USE_TZ = True
# Comment this when get Token by PostMan (Uncomment allow FrontEnd)
OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 36000,
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore'
}


OAUTH2_INFO = {
    "client_id": "4OG1rzVWWNjzi7LTBsHtjX3efhCdwzyOPr471JtH",
    "client_secret": "U3OYQqsOMVevk6WFXyf4rhTZbsGKUQ0yOAzZGREq6juNao5ORT81YPdmZcwJZzoJ0biCz6z2GSABeHL9YLOCeow1CBEwcktXqWdv1XcMOmYfj9K13vYYZMjLJDmwXy1t"
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]
CORS_ORIGIN_ALLOW_ALL=True
CORS_ORIGIN_WHITELIST = [
    'https://ipays.vn',
    'http://ipays.vn',
    'http://localhost']

CORS_ALLOW_ALL_ORIGINS = True # If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ['http://localhost','http://127.0.0.1','http://ipays.vn','https://ipays.vn']
CSRF_TRUSTED_ORIGINS = ['http://localhost']
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CORS_ALLOW_METHODS = ("DELETE","GET","OPTIONS","PATCH","POST","PUT",)
ALLOWED_HOSTS = ['192.168.1.5','localhost','http://ipays.vn','https://ipays.vn']
ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}
#############################################################
# LOGGING
#############################################################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{asctime:22.22s} {levelname:3.3s} {name} {funcName} {lineno}]: {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'ipays': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/chat.log',
            'formatter': 'verbose',
            'encoding': 'utf8',
            'backupCount': 3,
            'maxBytes': 1024*1024*1024
        },
        'django-info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/chat-info.log',
            'formatter': 'verbose',
            'level': 'INFO',
            'encoding': 'utf8',
            'backupCount': 3,
            'maxBytes': 1024*1024*1024
        },
        'django-debug': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/chat.log',
            'formatter': 'verbose',
            'encoding': 'utf8',
            'backupCount': 3,
            'maxBytes': 1024*1024*1024
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django.utils.autoreload': {
            'level': 'INFO',
        },
        'django': {
            'handlers': ['django-debug', 'django-info'],
            'level': env('DJANGO_LOG_LEVEL'),
            'propagate': False,
        },
        'ipays': {
            'handlers': ['console', 'ipays'],
            'level': env('DJANGO_LOG_LEVEL'),
            'propagate': False,
        }
    },
}
