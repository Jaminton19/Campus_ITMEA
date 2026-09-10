from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


# =====================================================
# SEGURIDAD
# =====================================================

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-itmea-campus-local'
)

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        'ALLOWED_HOSTS',
        'localhost,127.0.0.1'
    ).split(',')
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get(
        'CSRF_TRUSTED_ORIGINS',
        ''
    ).split(',')
    if origin.strip()
]


# =====================================================
# APLICACIONES
# =====================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
]


# =====================================================
# MIDDLEWARE
# =====================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Archivos estáticos para producción
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =====================================================
# URLS
# =====================================================

ROOT_URLCONF = 'itmea_platform.urls'


# =====================================================
# TEMPLATES
# =====================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [
            BASE_DIR / 'templates'
        ],

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


# =====================================================
# WSGI
# =====================================================

WSGI_APPLICATION = 'itmea_platform.wsgi.application'


# =====================================================
# BASE DE DATOS
# =====================================================

DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# =====================================================
# VALIDACIÓN DE CONTRASEÑAS
# =====================================================

AUTH_PASSWORD_VALIDATORS = []


# =====================================================
# IDIOMA Y ZONA HORARIA
# =====================================================

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True


# =====================================================
# ARCHIVOS ESTÁTICOS
# =====================================================

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'users/static'
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = (
    'whitenoise.storage.CompressedManifestStaticFilesStorage'
)


# =====================================================
# ARCHIVOS DE USUARIOS
# =====================================================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'


# =====================================================
# USUARIO PERSONALIZADO
# =====================================================

AUTH_USER_MODEL = 'users.User'


# =====================================================
# LOGIN
# =====================================================

LOGIN_REDIRECT_URL = 'dashboard'

LOGOUT_REDIRECT_URL = 'login'

LOGIN_URL = 'login'


# =====================================================
# CONFIGURACIÓN GENERAL
# =====================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =====================================================
# CORREO
# =====================================================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'