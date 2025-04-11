# bookstore_project/bookstore_project/settings.py

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/stable/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-YOUR_SECRET_KEY_HERE' # Replace with your actual secret key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',        # Core authentication framework
    'django.contrib.contenttypes',
    'django.contrib.sessions',    # Session framework
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store.apps.StoreConfig',     # Register our new 'store' app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', # Enables session support
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Associates users with requests using sessions
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bookstore_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Add the project-level templates directory
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True, # Allows Django to find templates inside app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Optional: context processor to make cart available globally
                'store.context_processors.cart_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'bookstore_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Use the MySQL database engine
        'NAME': 'sinhadb',          # Name of the database you created in MySQL
        'USER': 'root',        # Your MySQL database username
        'PASSWORD': '#HiMaNsHu123',   # Your MySQL database password
        'HOST': 'localhost',                  # Or the IP/hostname of your MySQL server (e.g., '127.0.0.1')
        'PORT': '3306',                       # Default MySQL port (can often be omitted if default)

        # Optional: Recommended settings for MySQL
        'OPTIONS': {
            # Set command to run when connection is established
            # Ensures strict SQL mode for data integrity
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            # Ensures proper handling of Unicode characters
            'charset': 'utf8mb4',
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # Keep the defaults or customize as needed
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

STATIC_URL = 'static/'
# Optional: Define where static files are collected during deployment
# STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Login/Logout Redirect URLs ---
LOGIN_URL = 'store:login'  # Redirect here if @login_required fails
LOGIN_REDIRECT_URL = 'store:book_list' # Redirect here after successful login
LOGOUT_REDIRECT_URL = 'store:book_list' # Redirect here after logout