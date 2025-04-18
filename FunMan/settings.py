from pathlib import Path
import os
import django_heroku


import environ
env = environ.Env()
environ.Env.read_env()


clientGoogleSECRET = env('CLIENT_GOOGLE_SECRET')
clientGoogleID = env('CLIENT_GOOGLE_ID')
clientGitHubSECRET = env('CLIENT_GITHUB_SECRET')
clientGitHubID = env('CLIENT_GITHUB_ID')
Email_Host_User = env('EMAIL_HOST_USER')
Email_Host_Password = env('EMAIL_HOST_PASSWORD')
UserFunbd = env('USERFUNDB')
PasswordFunbd = env('PASSWORDFUNDB')



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-93ui96b9h!p#hu)0vx1j(^1bi2@x5t46v5ixn$eo$gk7q#4&$='

# DEBUG
current_host = os.environ.get('HEROKU_APP_URL', 'http://127.0.0.1:8000')
if '127.0.0.1' in current_host or 'localhost' in current_host:
    DEBUG = True
else:
    DEBUG = False


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggit',
    'authorization',
    'home',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
]

ROOT_URLCONF = 'FunMan.urls'

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

WSGI_APPLICATION = 'FunMan.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'funbd',
        'USER': UserFunbd,
        'PASSWORD': PasswordFunbd,
        'HOST': 'localhost',
        'PORT': '5433',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# User
AUTH_USER_MODEL = 'authorization.MyUser'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': clientGoogleID,
            'secret': clientGoogleSECRET,
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'prompt': 'consent',    
        },
        'METHOD': 'oauth2',
        'VERIFIED_EMAIL': True,
    },
    'github': {
        'APP': {
            'client_id': clientGitHubID,
            'secret': clientGitHubSECRET,
        },
        'AUTH_PARAMS': {
            'prompt': 'consent',  
        },
    }
}

LOGIN_URL = '/authorization/'
LOGIN_REDIRECT_URL = '/'


SITE_ID = 1
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_UNIQUE_EMAIL = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"

SOCIALACCOUNT_ADAPTER = 'authorization.adapters.SocialAccountAdapter'

# MailGun
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = Email_Host_User
EMAIL_HOST_PASSWORD = Email_Host_Password



django_heroku.settings(locals())
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



django_heroku.settings(locals())

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



SILENCED_SYSTEM_CHECKS = ["auth.E003"] 
