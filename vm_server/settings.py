import os.path
from os.path import join
from pathlib import Path
from django.urls import reverse_lazy
from decouple import config, Csv


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# The url of the server, which is running inside the VM and accepts commands
url_of_server_on_vm = config('URL_OF_SERVER_ON_VM', default='')          # home1

# The location of the log for this server
location_for_the_log_file = config('LOCATION_FOR_THE_LOG_FILE', default='')

# The desired format of the logged date and time
desired_format_of_the_logged_date_and_time = config('DESIRED_FORMAT_OF_LOGGED_DATE_AND_TIME', default='')

"""
Add the ips below to ALLOWED_HOSTS and CORS_ALLOWED_ORIGINS
Add your IP to the field Host in Edit Configurations
Change the urls inside the react app not to 127.. but real ip in:
loginService.js, userService.js, vmService.js, App.js (for the login)
"""

# You should have host ip and the ips of the other computers in the network to grant access
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=Csv())

# Allow requests from React app during development
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='', cast=Csv())

# Optional: Allow credentials (e.g., cookies) to be sent with the requests
CORS_ALLOW_CREDENTIALS = True

# Allow specific HTTP methods (e.g., POST, PUT, DELETE)
CORS_ALLOW_METHODS = ['DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT',]

# Allow specific headers to be included in the requests
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',  # pip install django-cors-headers
    'rest_framework',

    'vm_server.main_app',
    'vm_server.user_management',
    'vm_server.virtual_machines',
    'vm_server.py_scripts',
    'vm_server.py_terminals',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware',  # Add this line before CommonMiddleware

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vm_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'vm_server.wsgi.application'

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

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = config('STATIC_URL', default='/static/')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
MEDIA_URL = config('MEDIA_URL', default='/media/')
MEDIA_ROOT = BASE_DIR / 'media_files'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""
To create superuser: python manage.py createsuperuser

For using the admin panel, there is a superuser:
username: daniel
email: daniel_zorov@abv.bg
password: Maimun06
"""
