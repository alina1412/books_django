from dotenv import load_dotenv
import os
from pathlib import Path

from urllib.parse import urlparse
# import django_heroku


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()


SECRET_KEY = os.environ.get("SECRET_KEY")
# POSTGRE_PASS = os.environ.get("POSTGRE_PASS")
# print(SECRET_KEY)


DEBUG = os.environ.get("IS_DEBUG") == 'True'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
# if DEBUG:
#     ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
# else:
#     ALLOWED_HOSTS = ['books-django-app.herokuapp.com']
# print(DEBUG)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'users.apps.UsersConfig',
    'shelves.apps.ShelvesConfig',

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

ROOT_URLCONF = 'books.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'static'],
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

WSGI_APPLICATION = 'books.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


def parse_db_url():
    db_url = os.environ.get("DATABASE_URL")
    db_url_parsed = urlparse(db_url)
    database = db_url_parsed.path[1:]
    credentals, address = db_url_parsed.netloc.split("@")
    uname, passwd = credentals.split(":")
    host, port = address.split(":")
    d = {"NAME": database,
         "USER": uname, "PASSWORD": passwd,
         "HOST": host, "PORT": port,
         "ENGINE": 'django.db.backends.postgresql_psycopg2',
         'OPTIONS': {'sslmode': 'disable'},
         }
    return d


if DEBUG:
    DATABASES = {
        # 'default': parse_db_url()
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': parse_db_url()
    }


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname) -8s %(module) -8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',   # for console
            'formatter': 'console'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': 'debug.log'
        }
    },
    'loggers': {
        '': {     # '<app-name>': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


STATIC_ROOT = BASE_DIR / 'static/'
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/css/"),
    os.path.join(BASE_DIR, "static/img/"),
    os.path.join(BASE_DIR, "static/templates/"),
]

# print('BASE_DIR', BASE_DIR, f'{BASE_DIR}/static/templates/')
# TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'dbroutes/static/templates'),
# os.path.join(BASE_DIR, 'users/templates/')]


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# print("2", DATABASES)
# if not DEBUG:
#     django_heroku.settings(locals())

# print("3", DATABASES)
