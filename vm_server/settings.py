import os.path
from os.path import join
from pathlib import Path
from django.urls import reverse_lazy


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&eteg8**+jh+x1ziy789bh^ppcgxyk5w4dj@ikc@ap-3ejuxvp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ---------------------------------------------------------------------------------
# Global variables
# ---------------------------------------------------------------------------------
virtual_machine_name = 'VM000180'
location_of_server_code_folder = 'C:\\Users\\User\\Desktop\\server_code'

url_of_server_on_vm = 'http://192.168.56.101:5000/command'   # home1
# url_of_server_on_vm = 'http://127.0.0.1:5000/command'      # home2
# url_of_server_on_vm = 'http://172.23.139.29:5000/command'  # when on festo wifi and after changing the ip of the vm
# url_of_server_on_vm = 'http://172.23.123.57:5000/command'  # when on new office wifi and after changing the ip of the vm

location_for_the_log_file = 'log.txt'
desired_format_of_the_logged_date_and_time = "%d/%m/%Y %H:%M:%S"

# ---------------------------------------------------------------------------------
# IP addresses
# ---------------------------------------------------------------------------------
"""
Add the ips below to ALLOWED_HOSTS and CORS_ALLOWED_ORIGINS
Add your IP to the field Host in Edit Configurations
Change the urls inside the react app not to 127.. but real ip in:
    loginService.js, userService.js, vmService.js, App.js (for the login)
"""

ALLOWED_HOSTS = [
    'localhost',
    '0.0.0.0',          # added
    '127.0.0.1',
    # '172.23.139.33',    # added my ip in the network of old office
    '172.23.123.57',    # added my ip in the network of new office
    # '172.23.139.27',    # external ip Mariyan old office
    # '172.23.138.56',    # external ip Georgi old office
    '172.23.122.102',   # external ip Mariyan new office
    '172.23.122.107',   # external ip Georgi new office
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",        # Allow requests from React app during development
    # "http://172.23.139.33:3000",  # Allow requests from React app during development in old office
    "http://172.23.123.57:3000",    # Allow requests from React app during development in new office
]

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

# -------------------------------------------------------------------
# Application definition

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


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# postgresql
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'vm_server_db',         # same name as the DB created
#         'USER': 'postgres-user',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',    # Not host.docker.internal - only for pgadmin
#         'PORT': '5432',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media_files'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""
Create superuser:
python manage.py createsuperuser
"""
