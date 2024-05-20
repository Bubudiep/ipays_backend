from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
import os, environ
env = environ.Env(
    DJANGO_LOG_LEVEL=(str, 'DEBUG'),
)
import mimetypes
mimetypes.add_type("text/css", ".css", True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


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
    'oauth2_provider',
    'corsheaders',
]
WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'  # new
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
    "client_id": "EcLPNRzCUOUOl7YmEAuN6lY99qaKbQ2kC0jK3kzR",
    "client_secret": "9e77jSvVMcV3BxsY51cAlzYTW9OtLsqZLp2mxHc2gb7xQEj3IEtUjHTWDffwrAmXLIJfAz2WtmuKIJIWfUxMkzqTc7KpPE96AmHijdkLyi0FXGOkGebWVBHvVpRAfWyT"
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
    'http://localhost','http://127.0.0.1',
    'http://171.228.191.130',
    'http://171.228.191.130:8000']

CORS_ALLOW_ALL_ORIGINS = False # If this is used then `CORS_ALLOWED_ORIGINS` will not have any effect
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ['http://localhost','http://127.0.0.1','http://ipays.vn','https://ipays.vn','http://171.228.191.130',
    'http://171.228.191.130:8000']
CSRF_TRUSTED_ORIGINS = ['http://localhost','http://171.228.191.130','http://127.0.0.1',
    'http://171.228.191.130:8000']
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CORS_ALLOW_METHODS = ("DELETE","GET","OPTIONS","PATCH","POST","PUT",)
ALLOWED_HOSTS = ['192.168.1.5','localhost','http://ipays.vn','https://ipays.vn','171.228.191.130','127.0.0.1',
    '171.228.191.130:8000']
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
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'ipays',
        'USER': 'root',
        'PASSWORD': 'Pan123456!!',
        'HOST': 'localhost',
        'PORT': '3306',
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
DATA_UPLOAD_MAX_NUMBER_FIELDS = 100000000 # higher than the count of fields
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT=os.path.join(BASE_DIR, "staticfiles")
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
