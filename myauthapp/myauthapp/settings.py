from pathlib import Path
import os
from dotenv import load_dotenv
import idna 

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

env_path = BASE_DIR / '.env'
load_dotenv(env_path)

SECRET_KEY='django-insecure-m3%!16-+$j*%-!n6l=s3id^oo_qfsm^sx#=eo#s_9fz6^xdiib'


def convert_idn_email(email):
    try:
        if '@' in email:
            local_part, domain = email.split('@')
            domain_ascii = idna.encode(domain).decode('ascii')
            return f"{local_part}@{domain_ascii}"
        return email
    except:
        return email

ASCII_EMAIL = convert_idn_email('email@хронопунктура.рф')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False').lower() == 'true'
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'False').lower() == 'true'
EMAIL_HOST_USER = ASCII_EMAIL
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')


ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'application',
    'payments',
    'week_prediction',
    'subscription',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myauthapp.urls'

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
                
                'payments.context_processors.subscription_status',
              	'accounts.context_processors.email_settings',
            ],
        },
    },
]

WSGI_APPLICATION = 'myauthapp.wsgi.application'

DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


if DEBUG:
    STATIC_URL = 'myauthapp/staticfiles/static/'
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]

else:
    STATIC_URL = 'myauthapp/staticfiles/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

AUTH_USER_MODEL = 'accounts.CustomUser'


YOOKASSA_SHOP_ID = '1127478'  
YOOKASSA_SECRET_KEY = 'test_RojrVAuhuf5dVwSYDkuy-AMITYoTJCXE49yeSPu7dSs' 


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache", 
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}